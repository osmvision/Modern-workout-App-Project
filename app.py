import streamlit as st
import utils
import pandas as pd
from datetime import datetime, timedelta
import random
from exercise_library import (
    EXERCISE_LIBRARY, EXERCISE_CATEGORIES, DIFFICULTY_LEVELS,
    search_exercises
)
# IMPORTER LA NOUVELLE LIBRAIRIE CALENDRIER
from streamlit_calendar import calendar

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Jade Fitness Hub", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GESTION DE L'ÉTAT (SESSION STATE) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'nav_page' not in st.session_state:
    st.session_state.nav_page = "🏠 Home"
if 'page_history' not in st.session_state:
    st.session_state.page_history = []

# --- 3. FONCTIONS DE NAVIGATION ---
def navigate_to(target_page):
    """Va vers une page et sauvegarde l'actuelle dans l'historique"""
    if st.session_state.nav_page != target_page:
        st.session_state.page_history.append(st.session_state.nav_page)
        st.session_state.nav_page = target_page
        st.rerun()

def go_back():
    """Revient à la page précédente"""
    if st.session_state.page_history:
        previous_page = st.session_state.page_history.pop()
        st.session_state.nav_page = previous_page
        st.rerun()
    else:
        st.session_state.nav_page = "🏠 Home"
        st.rerun()

# --- 4. CSS (DESIGN & MOBILE FIX) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Fond général */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #1b263b 100%);
        background-attachment: fixed;
    }
    
    /* Textes et Titres */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; color: #caf0f8 !important; }
    p, div, label, span { font-family: 'Rajdhani', sans-serif; color: #90e0ef; }
    
    /* Boutons stylisés */
    .stButton > button {
        background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        transition: all 0.3s ease;
    }

    /* --- MOBILE OPTIMIZATION --- */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] { display: none !important; }
        .main .block-container { padding-bottom: 100px !important; }
        
        .mobile-nav-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(180deg, rgba(13, 27, 42, 0.95), #050a14);
            backdrop-filter: blur(10px);
            border-top: 1px solid #00d4ff;
            z-index: 99999;
            padding: 10px 5px;
        }
        
        /* Force horizontal alignment */
        div[data-testid="column"] {
            flex: 1 !important; 
            min-width: 0 !important;
        }
        
        .mobile-nav-container button {
            padding: 5px !important;
            font-size: 1.5rem !important;
            line-height: 1 !important;
            margin: 0 !important;
        }
    }
    
    @media (min-width: 769px) {
        .mobile-nav-container { display: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- 5. PAGE DE LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>💎 JADE FITNESS</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            password = st.text_input("🔐 Enter PIN", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                if password in ["1234", "jade", ""]:
                    st.session_state.logged_in = True
                    try:
                        utils.init_calendar()
                        utils.populate_sample_workouts()
                    except: pass
                    st.rerun()
                else:
                    st.error("❌ Incorrect PIN")
    st.stop()

# --- 6. SIDEBAR (PC) ---
with st.sidebar:
    st.markdown("## 💎 JADE")
    st.markdown("---")
    nav_items = ["🏠 Home", "📅 Workout Calendar", "💪 Workout Programs", "📚 Exercise Library", "🎬 My Collection"]
    current_idx = nav_items.index(st.session_state.nav_page) if st.session_state.nav_page in nav_items else 0
    selected = st.radio("Menu", nav_items, index=current_idx)
    if selected != st.session_state.nav_page: navigate_to(selected)
    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 7. BOUTON RETOUR ---
if st.session_state.nav_page != "🏠 Home":
    if st.button("⬅️ Retour", key="top_back"):
        go_back()

# --- 8. CONTENU DES PAGES ---
page = st.session_state.nav_page

# ===== PAGE: HOME =====
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">💎 JADE FITNESS HUB</h1>', unsafe_allow_html=True)
    
    try:
        streak_data = utils.get_streak_data()
        c1, c2 = st.columns(2)
        c1.metric("🔥 Streak", f"{streak_data.get('current_streak', 0)} Days")
        c2.metric("🏆 Best", f"{streak_data.get('best_streak', 0)} Days")
    except:
        st.info("Start training!")

    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    c1, c2, c3 = st.columns(3)
    if c1.button("📅 Calendar", use_container_width=True): navigate_to("📅 Workout Calendar")
    if c2.button("💪 Programs", use_container_width=True): navigate_to("💪 Workout Programs")
    if c3.button("🎬 Videos", use_container_width=True): navigate_to("🎬 My Collection")

# ===== PAGE: CALENDAR (NOUVEAU SYSTÈME) =====
elif page == "📅 Workout Calendar":
    st.markdown('<h1>📅 WORKOUT CALENDAR</h1>', unsafe_allow_html=True)
    
    # 1. Chargement des données
    try:
        utils.init_calendar()
        raw_data = utils.load_calendar()
    except:
        raw_data = {}

    # 2. Conversion des données pour streamlit-calendar
    calendar_events = []
    for date_str, workouts in raw_data.items():
        for w in workouts:
            # Couleur verte si fini, orange si prévu
            color = "#00ff88" if w.get('completed', False) else "#ffaa00"
            calendar_events.append({
                "title": f"{'✅' if w.get('completed') else '⏳'} {w.get('name')}",
                "start": date_str,
                "backgroundColor": color,
                "borderColor": color,
                "allDay": True
            })

    # 3. Configuration du calendrier
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,listMonth"
        },
        "initialView": "dayGridMonth",
        "height": "650px",
        "contentHeight": "auto",
        "themeSystem": "standard" # Utilise le CSS Streamlit
    }
    
    # 4. Affichage du calendrier interactif
    # custom_css permet de styliser le calendrier pour qu'il soit 'Dark Mode'
    custom_css = """
        .fc-theme-standard td, .fc-theme-standard th { border-color: #00d4ff; }
        .fc-daygrid-day-number { color: #caf0f8; text-decoration: none; }
        .fc-col-header-cell-cushion { color: #00d4ff; }
        .fc-toolbar-title { color: #ffffff !important; font-family: 'Orbitron', sans-serif; }
        .fc-button { background-color: #0077b6 !important; border: none; }
    """
    
    calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)

    st.markdown("---")
    st.markdown("### ➕ Add Workout Manually")
    with st.form("new_workout"):
        c1, c2 = st.columns(2)
        d = c1.date_input("Date", datetime.now())
        n = c2.text_input("Workout Name")
        if st.form_submit_button("Save Workout", use_container_width=True):
            if n:
                utils.add_workout_to_calendar(d.strftime("%Y-%m-%d"), {"name": n, "completed": False})
                st.success("Workout Added!")
                st.rerun()

# ===== PAGE: PROGRAMS =====
elif page == "💪 Workout Programs":
    st.markdown('<h1>💪 PROGRAMS</h1>', unsafe_allow_html=True)
    programs = utils.get_workout_programs()
    for pid, p in programs.items():
        with st.expander(f"📌 {p['name']} ({p['level']})"):
            st.write(p['description'])
            if st.button("Start Program", key=pid):
                st.success(f"Started {p['name']}!")

# ===== PAGE: LIBRARY =====
elif page == "📚 Exercise Library":
    st.markdown('<h1>📚 LIBRARY</h1>', unsafe_allow_html=True)
    search = st.text_input("🔍 Search Exercise")
    if search:
        results = search_exercises(search)
        st.write(f"Found {len(results)} exercises")
    else:
        st.info("Type to search exercises...")

# ===== PAGE: COLLECTION =====
elif page == "🎬 My Collection":
    st.markdown('<h1>🎬 COLLECTION</h1>', unsafe_allow_html=True)
    url = st.text_input("Paste YouTube URL")
    cat = st.selectbox("Category", ["Strength", "Cardio", "Yoga"])
    if st.button("Add Video"):
        if url:
            try:
                utils.add_workout(url, cat)
                st.success("Video Added!")
                st.rerun()
            except: st.error("Error")
    
    st.markdown("---")
    df = utils.get_workouts()
    if not df.empty:
        for i, row in df.iterrows():
            with st.expander(f"📺 {row['title']}"):
                st.video(row['url'])
                if st.button("Delete", key=f"del_{i}"):
                    # Ajouter logique de suppression si besoin
                    st.rerun()

# --- 9. NAVIGATION MOBILE (HORIZONTAL FIXED) ---
st.markdown('<div class="mobile-nav-container">', unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    if st.button("🏠", key="m1", help="Home", use_container_width=True): navigate_to("🏠 Home")
with cols[1]:
    if st.button("📅", key="m2", help="Cal", use_container_width=True): navigate_to("📅 Workout Calendar")
with cols[2]:
    if st.button("💪", key="m3", help="Prog", use_container_width=True): navigate_to("💪 Workout Programs")
with cols[3]:
    if st.button("📚", key="m4", help="Lib", use_container_width=True): navigate_to("📚 Exercise Library")
with cols[4]:
    if st.button("🎬", key="m5", help="Vid", use_container_width=True): navigate_to("🎬 My Collection")
st.markdown('</div>', unsafe_allow_html=True)