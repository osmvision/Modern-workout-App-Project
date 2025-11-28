import streamlit as st
import utils
import pandas as pd
from datetime import datetime, timedelta
import calendar
import random
from exercise_library import (
    EXERCISE_LIBRARY, EXERCISE_CATEGORIES, DIFFICULTY_LEVELS,
    search_exercises
)

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Jade Fitness Hub", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GESTION DE L'ÉTAT (SESSION STATE) ---
# Initialisation des variables pour qu'elles existent dès le début
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'nav_page' not in st.session_state:
    st.session_state.nav_page = "🏠 Home"
if 'page_history' not in st.session_state:
    st.session_state.page_history = [] # Historique pour le bouton Retour
if 'calendar_month' not in st.session_state:
    st.session_state.calendar_month = datetime.now().month
if 'calendar_year' not in st.session_state:
    st.session_state.calendar_year = datetime.now().year

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
    p, div, label { font-family: 'Rajdhani', sans-serif; color: #90e0ef; }
    
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
        /* Cacher la Sidebar native sur mobile */
        section[data-testid="stSidebar"] { display: none !important; }
        
        /* Laisser de la place en bas pour la barre de nav */
        .main .block-container { padding-bottom: 100px !important; }
        
        /* Conteneur de la barre du bas */
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
        
        /* FORCE L'ALIGNEMENT HORIZONTAL DES COLONNES */
        .mobile-nav-content {
            display: flex !important;
            flex-direction: row !important;
            justify-content: space-around !important;
            align-items: center !important;
            width: 100% !important;
        }
        
        /* Ajustement des boutons dans la barre */
        .mobile-nav-content button {
            background: transparent !important;
            box-shadow: none !important;
            padding: 5px !important;
            font-size: 1.5rem !important;
            min-height: auto !important;
        }
    }
    
    /* Cacher la barre mobile sur PC */
    @media (min-width: 769px) {
        .mobile-nav-container { display: none !important; }
    }
    
    /* Style du Calendrier */
    .cal-day-box {
        background: rgba(0, 119, 182, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        min-height: 80px;
    }
    .cal-day-box.today { border: 2px solid #00d4ff; background: rgba(0, 180, 216, 0.2); }
</style>
""", unsafe_allow_html=True)

# --- 5. PAGE DE LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>💎 JADE FITNESS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your Transformation Starts Here</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            password = st.text_input("🔐 Enter PIN", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if password in ["1234", "jade", ""]:
                    st.session_state.logged_in = True
                    # Initialisation sécurisée du calendrier
                    try:
                        utils.init_calendar()
                        utils.populate_sample_workouts()
                    except:
                        pass 
                    st.rerun()
                else:
                    st.error("❌ Incorrect PIN")
    st.stop()

# --- 6. SIDEBAR (PC UNIQUEMENT) ---
with st.sidebar:
    st.markdown("## 💎 JADE")
    st.markdown(f"Bonjour, Jade! {datetime.now().strftime('%H:%M')}")
    st.markdown("---")
    
    # Navigation PC
    nav_items = ["🏠 Home", "📅 Workout Calendar", "💪 Workout Programs", "📚 Exercise Library", "🎬 My Collection"]
    
    # On trouve l'index actuel
    current_index = 0
    if st.session_state.nav_page in nav_items:
        current_index = nav_items.index(st.session_state.nav_page)
        
    selected = st.radio("Menu", nav_items, index=current_index)
    
    if selected != st.session_state.nav_page:
        navigate_to(selected)
        
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# --- 7. HEADER & BOUTON RETOUR ---
# Afficher le bouton retour si on n'est pas sur la Home
if st.session_state.nav_page != "🏠 Home":
    if st.button("⬅️ Retour", key="top_back_btn"):
        go_back()

# --- 8. CONTENU DES PAGES ---
page = st.session_state.nav_page

# ===== PAGE: HOME =====
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">💎 JADE FITNESS HUB 💎</h1>', unsafe_allow_html=True)
    
    # Stats Rapides
    try:
        streak_data = utils.get_streak_data()
        c1, c2 = st.columns(2)
        c1.metric("🔥 Streak", f"{streak_data.get('current_streak', 0)} Days")
        c2.metric("🏆 Best", f"{streak_data.get('best_streak', 0)} Days")
    except:
        st.info("Welcome! Start your first workout.")

    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📅 Calendar", use_container_width=True): navigate_to("📅 Workout Calendar")
    with c2:
        if st.button("💪 Programs", use_container_width=True): navigate_to("💪 Workout Programs")
    with c3:
        if st.button("🎬 Videos", use_container_width=True): navigate_to("🎬 My Collection")

# ===== PAGE: CALENDAR =====
elif page == "📅 Workout Calendar":
    st.markdown('<h1>📅 CALENDAR</h1>', unsafe_allow_html=True)
    
    # Navigation Mois
    c_prev, c_label, c_next = st.columns([1, 3, 1])
    with c_prev:
        if st.button("◀️"):
            if st.session_state.calendar_month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year -= 1
            else:
                st.session_state.calendar_month -= 1
            st.rerun()
            
    with c_label:
        month_name = calendar.month_name[st.session_state.calendar_month]
        st.markdown(f"<h3 style='text-align: center'>{month_name} {st.session_state.calendar_year}</h3>", unsafe_allow_html=True)
        
    with c_next:
        if st.button("▶️"):
            if st.session_state.calendar_month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year += 1
            else:
                st.session_state.calendar_month += 1
            st.rerun()

    # Logique du Calendrier
    try:
        utils.init_calendar()
        calendar_data = utils.load_calendar()
    except:
        calendar_data = {}

    cal = calendar.Calendar(firstweekday=6) # Dimanche premier jour
    month_days = cal.monthdayscalendar(st.session_state.calendar_year, st.session_state.calendar_month)
    
    # Affichage des Jours
    days_cols = st.columns(7)
    days_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for idx, day_name in enumerate(days_names):
        days_cols[idx].markdown(f"**{day_name}**")
        
    for week in month_days:
        week_cols = st.columns(7)
        for idx, day_num in enumerate(week):
            with week_cols[idx]:
                if day_num != 0:
                    # Construction de la date
                    date_str = f"{st.session_state.calendar_year}-{st.session_state.calendar_month:02d}-{day_num:02d}"
                    is_today = (day_num == datetime.now().day and 
                               st.session_state.calendar_month == datetime.now().month and 
                               st.session_state.calendar_year == datetime.now().year)
                    
                    has_workout = date_str in calendar_data and len(calendar_data[date_str]) > 0
                    
                    # Style visuel
                    bg_style = "border: 2px solid #00d4ff;" if is_today else "border: 1px solid rgba(255,255,255,0.1);"
                    icon = "🔥" if has_workout else "💤"
                    
                    st.markdown(f"""
                    <div style="{bg_style} border-radius: 8px; padding: 5px; text-align: center; min-height: 60px; background: rgba(0,0,0,0.2);">
                        <div style="font-weight: bold; color: #caf0f8;">{day_num}</div>
                        <div style="font-size: 1.2rem;">{icon}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")

    st.markdown("---")
    st.markdown("### ➕ Add Workout")
    with st.form("add_w"):
        d = st.date_input("Date", datetime.now())
        n = st.text_input("Workout Name")
        if st.form_submit_button("Save"):
            try:
                utils.add_workout_to_calendar(d.strftime("%Y-%m-%d"), {"name": n, "completed": False})
                st.success("Saved!")
                st.rerun()
            except:
                st.error("Error saving")

# ===== PAGE: PROGRAMS =====
elif page == "💪 Workout Programs":
    st.markdown('<h1>💪 PROGRAMS</h1>', unsafe_allow_html=True)
    try:
        programs = utils.get_workout_programs()
        for pid, p in programs.items():
            with st.expander(f"📌 {p['name']} ({p['level']})"):
                st.write(p['description'])
                st.write(f"⏱️ {p['duration']} | 🗓️ {p['days_per_week']} days/week")
                if st.button("Start This Program", key=pid):
                    st.success(f"Program {p['name']} activated!")
    except:
        st.info("Loading programs...")

# ===== PAGE: LIBRARY =====
elif page == "📚 Exercise Library":
    st.markdown('<h1>📚 LIBRARY</h1>', unsafe_allow_html=True)
    query = st.text_input("🔍 Search Exercise")
    
    if query:
        st.info(f"Searching for: {query}...")
        # Ici on simule, vous pouvez connecter votre fonction search_exercises
        results = search_exercises(query) if 'search_exercises' in globals() else {}
    
    st.write("Browse categories below:")
    cats = EXERCISE_CATEGORIES if 'EXERCISE_CATEGORIES' in globals() else ["Strength", "Cardio", "Yoga"]
    selected_cat = st.selectbox("Category", cats)
    st.write(f"Showing exercises for: {selected_cat}")

# ===== PAGE: COLLECTION =====
elif page == "🎬 My Collection":
    st.markdown('<h1>🎬 COLLECTION</h1>', unsafe_allow_html=True)
    
    st.markdown("### Add New Video")
    url = st.text_input("Paste YouTube URL")
    cat = st.selectbox("Type", ["Strength", "Cardio", "Yoga", "HIIT"])
    
    if st.button("Add Video"):
        if url:
            try:
                utils.add_workout(url, cat)
                st.success("Video added!")
            except:
                st.error("Could not add video")
    
    st.markdown("---")
    st.markdown("### Your Videos")
    try:
        df = utils.get_workouts()
        if not df.empty:
            for i, row in df.iterrows():
                with st.expander(f"📺 {row['title']}"):
                    st.video(row['url'])
                    if st.button("Delete", key=f"del_{i}"):
                        # Logique de suppression à ajouter dans utils
                        st.rerun()
        else:
            st.info("No videos yet.")
    except:
        st.write("Library empty.")

# --- 9. BARRE DE NAVIGATION MOBILE (FIXED HORIZONTAL) ---
# Ce conteneur est caché sur PC via CSS, et forcé en ligne (row) sur mobile
st.markdown('<div class="mobile-nav-container"><div class="mobile-nav-content">', unsafe_allow_html=True)

# On utilise des colonnes Streamlit mais le CSS "mobile-nav-content" va gérer l'affichage
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠", key="m_home", help="Home", use_container_width=True):
        navigate_to("🏠 Home")
with col2:
    if st.button("📅", key="m_cal", help="Calendar", use_container_width=True):
        navigate_to("📅 Workout Calendar")
with col3:
    if st.button("💪", key="m_prog", help="Programs", use_container_width=True):
        navigate_to("💪 Workout Programs")
with col4:
    if st.button("📚", key="m_lib", help="Library", use_container_width=True):
        navigate_to("📚 Exercise Library")
with col5:
    if st.button("🎬", key="m_col", help="Videos", use_container_width=True):
        navigate_to("🎬 My Collection")

st.markdown('</div></div>', unsafe_allow_html=True)