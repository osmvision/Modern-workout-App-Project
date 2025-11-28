import streamlit as st
import utils
import pandas as pd
from datetime import datetime, timedelta
import calendar
import random
from exercise_library import (
    EXERCISE_LIBRARY, EXERCISE_CATEGORIES, DIFFICULTY_LEVELS,
    MIXAMO_RESOURCES, get_exercises_by_category, get_exercises_by_difficulty,
    search_exercises, get_all_muscle_groups
)
import streamlit.components.v1 as components

# --- 1. CONFIGURATION ---
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
# Initialisation du calendrier pour éviter les crashs
if 'calendar_month' not in st.session_state:
    st.session_state.calendar_month = datetime.now().month
if 'calendar_year' not in st.session_state:
    st.session_state.calendar_year = datetime.now().year

# --- 3. FONCTIONS DE NAVIGATION ---
def navigate_to(page_name):
    """Change de page et sauvegarde l'historique"""
    if st.session_state.nav_page != page_name:
        st.session_state.page_history.append(st.session_state.nav_page)
        st.session_state.nav_page = page_name
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

# --- 4. CSS (DESIGN ORIGINAL + FIX MOBILE) ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Main Background - Deep Space Blue */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #1b263b 100%);
        background-attachment: fixed;
    }
    
    /* Text Styling */
    h1, h2, h3, h4 { font-family: 'Orbitron', sans-serif !important; color: #caf0f8 !important; }
    p, .stMarkdown { font-family: 'Rajdhani', sans-serif; color: #90e0ef; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 25px !important;
        transition: all 0.3s ease !important;
    }

    /* --- MOBILE NAVIGATION FIX (HORIZONTAL) --- */
    .mobile-nav-container { display: none; } /* Hidden on PC */

    @media (max-width: 768px) {
        /* Hide Sidebar */
        section[data-testid="stSidebar"] { display: none !important; }
        
        /* Show Bottom Bar */
        .mobile-nav-container {
            display: block;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(180deg, rgba(10, 15, 30, 0.98) 0%, #050a14 100%);
            border-top: 1px solid rgba(0, 212, 255, 0.4);
            z-index: 99999;
            padding: 5px;
            box-shadow: 0 -5px 20px rgba(0,0,0,0.5);
        }

        /* FORCE HORIZONTAL ALIGNMENT FOR COLUMNS */
        div[data-testid="column"] {
            width: 20% !important;
            flex: 1 1 auto !important;
            min-width: 50px !important;
            display: flex !important;
            flex-direction: column !important;
        }

        /* Adjust Buttons */
        .mobile-nav-container .stButton button {
            width: 100%;
            padding: 0.5rem 0;
            font-size: 1.5rem; /* Bigger emojis */
            line-height: 1;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            margin: 0 !important;
        }
        
        /* Spacing for content */
        .main .block-container { padding-bottom: 100px !important; }
    }
    
    /* Calendar Styles (Original) */
    .cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; margin: 10px 0; }
    .cal-header { text-align: center; padding: 8px 4px; color: #00d4ff; font-family: 'Orbitron'; font-size: 0.8rem; background: rgba(0, 119, 182, 0.2); border-radius: 5px; }
    .cal-day { text-align: center; padding: 8px 4px; min-height: 50px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .cal-day-num { font-family: 'Orbitron'; font-size: 0.9rem; }
    .cal-day-normal { background: rgba(0, 119, 182, 0.1); border: 1px solid rgba(0, 212, 255, 0.2); color: #caf0f8; }
    .cal-day-today { background: rgba(0, 180, 216, 0.3); border: 2px solid #00d4ff; color: #00d4ff; font-weight: 700; }
    .cal-day-workout { background: rgba(0, 212, 255, 0.15); border: 2px solid rgba(0, 212, 255, 0.5); color: #90e0ef; }
    .cal-day-completed { background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(0, 255, 136, 0.1)); border: 2px solid #ffa500; color: #ffa500; }
</style>
""", unsafe_allow_html=True)

# --- EXERCISE GIF VIEWER ---
def render_exercise_demo(exercise_name="Exercise", exercise_type="general"):
    EXERCISE_GIFS = {
        "squats": "https://fitnessprogramer.com/wp-content/uploads/2021/02/SQUAT.gif",
        "push_up": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-up.gif",
        "plank": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Front-Plank.gif",
        "burpee": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Burpee.gif",
        "default": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-jack.gif"
    }
    exercise_key = exercise_name.lower().replace(" ", "_").replace("-", "_")
    gif_url = EXERCISE_GIFS.get(exercise_key, EXERCISE_GIFS.get("default"))
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0, 30, 60, 0.9) 0%, rgba(0, 60, 90, 0.8) 100%); border-radius: 15px; border: 2px solid rgba(0, 212, 255, 0.3); padding: 15px;">
        <div style="text-align: center; font-family: 'Orbitron'; color: #00d4ff; margin-bottom: 10px;">🏃‍♀️ {exercise_name}</div>
        <img src="{gif_url}" style="width: 100%; max-height: 300px; object-fit: contain; border-radius: 10px;">
    </div>
    """, unsafe_allow_html=True)

# --- LOGIN ---
def show_login_page():
    st.markdown("<br><br><h1 style='text-align: center; color: #00d4ff;'>💎 JADE FITNESS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("🔐 PIN", type="password")
        if st.button("Enter", use_container_width=True):
            if password in ["1234", "jade", ""]:
                st.session_state.logged_in = True
                try:
                    utils.init_calendar()
                    utils.populate_sample_workouts()
                except: pass
                st.rerun()
            else:
                st.error("Incorrect PIN")

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# --- SIDEBAR (PC) ---
with st.sidebar:
    st.markdown("## 💎 JADE")
    st.markdown("---")
    nav_options = ["🏠 Home", "📅 Workout Calendar", "💪 Workout Programs", "📚 Exercise Library", "🎬 My Collection"]
    current_index = 0
    if st.session_state.nav_page in nav_options:
        current_index = nav_options.index(st.session_state.nav_page)
    
    selected = st.radio("Menu", nav_options, index=current_index)
    if selected != st.session_state.nav_page:
        navigate_to(selected)
    
    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- BOUTON RETOUR (BACK) ---
# Affiche le bouton retour sur toutes les pages sauf Home
if st.session_state.nav_page != "🏠 Home":
    if st.button("⬅️ Retour", key="back_btn"):
        go_back()

# --- MAIN CONTENT ---
page = st.session_state.nav_page

# ===== HOME PAGE =====
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">💎 JADE FITNESS HUB</h1>', unsafe_allow_html=True)
    
    # Welcome
    st.markdown(f"""
    <div style="background: rgba(0, 180, 216, 0.1); border: 1px solid #00d4ff; border-radius: 20px; padding: 20px; margin: 20px 0;">
        <p style="color: #caf0f8; font-size: 1.2rem; margin: 0;">Welcome back, <strong>Jade</strong>! Ready to crush it? 💪</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("## ⚡ Quick Actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📅 Plan Workout", use_container_width=True): navigate_to("📅 Workout Calendar")
    with c2:
        if st.button("💪 Programs", use_container_width=True): navigate_to("💪 Workout Programs")
    with c3:
        if st.button("🎬 My Videos", use_container_width=True): navigate_to("🎬 My Collection")

# ===== CALENDAR PAGE (FIXED LOGIC) =====
elif page == "📅 Workout Calendar":
    st.markdown('<h1 class="main-header">📅 CALENDAR</h1>', unsafe_allow_html=True)
    
    # Load Data
    try:
        utils.init_calendar()
        calendar_data = utils.load_calendar()
    except:
        calendar_data = {}

    # Navigation Controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀️ Prev"):
            if st.session_state.calendar_month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year -= 1
            else:
                st.session_state.calendar_month -= 1
            st.rerun()
    with col2:
        month_name = calendar.month_name[st.session_state.calendar_month]
        st.markdown(f"<h3 style='text-align: center; color: #00d4ff;'>{month_name} {st.session_state.calendar_year}</h3>", unsafe_allow_html=True)
    with col3:
        if st.button("Next ▶️"):
            if st.session_state.calendar_month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year += 1
            else:
                st.session_state.calendar_month += 1
            st.rerun()

    # Generate HTML Calendar
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(st.session_state.calendar_year, st.session_state.calendar_month)
    days_header = ["S", "M", "T", "W", "T", "F", "S"]
    today = datetime.now()
    
    html = '<div class="cal-grid">'
    for d in days_header:
        html += f'<div class="cal-header">{d}</div>'
    
    for week in month_days:
        for day in week:
            if day == 0:
                html += '<div class="cal-day" style="background: transparent;"></div>'
            else:
                date_str = f"{st.session_state.calendar_year}-{st.session_state.calendar_month:02d}-{day:02d}"
                is_today = (day == today.day and st.session_state.calendar_month == today.month and st.session_state.calendar_year == today.year)
                has_workouts = date_str in calendar_data and len(calendar_data[date_str]) > 0
                
                # Logic for style
                style_class = "cal-day-normal"
                icon = ""
                if is_today: style_class = "cal-day-today"
                elif has_workouts: 
                    style_class = "cal-day-workout"
                    icon = "💪"
                
                html += f'<div class="cal-day {style_class}"><div class="cal-day-num">{day}</div><div style="font-size:0.8rem">{icon}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

    # Add Workout Form
    st.markdown("### ➕ Add Workout")
    c1, c2 = st.columns(2)
    with c1:
        sel_date = st.date_input("Date", datetime.now())
    with c2:
        w_name = st.text_input("Workout Name")
    
    if st.button("Save Workout", use_container_width=True):
        if w_name:
            d_str = sel_date.strftime("%Y-%m-%d")
            try:
                utils.add_workout_to_calendar(d_str, {"name": w_name, "completed": False})
                st.success("Saved!")
                st.rerun()
            except:
                st.error("Error saving")

# ===== PROGRAMS PAGE =====
elif page == "💪 Workout Programs":
    st.markdown('<h1 class="main-header">💪 PROGRAMS</h1>', unsafe_allow_html=True)
    try:
        programs = utils.get_workout_programs()
        for pid, p in programs.items():
            with st.expander(f"📌 {p['name']} ({p['level']})"):
                st.write(p['description'])
                if st.button("View Details", key=pid):
                    st.info(f"Duration: {p['duration']}")
    except:
        st.info("Loading programs...")

# ===== LIBRARY PAGE =====
elif page == "📚 Exercise Library":
    st.markdown('<h1 class="main-header">📚 LIBRARY</h1>', unsafe_allow_html=True)
    search = st.text_input("🔍 Search")
    if search:
        results = search_exercises(search)
        st.write(f"Found {len(results)} exercises")
    else:
        exercises = list(EXERCISE_LIBRARY.items())[:6] # Show first 6
        for k, v in exercises:
            with st.expander(v['name']):
                render_exercise_demo(v['name'])

# ===== COLLECTION PAGE =====
elif page == "🎬 My Collection":
    st.markdown('<h1 class="main-header">🎬 COLLECTION</h1>', unsafe_allow_html=True)
    url = st.text_input("Paste YouTube URL")
    cat = st.selectbox("Category", ["Strength", "Cardio", "Yoga"])
    if st.button("Add Video"):
        if url:
            try:
                utils.add_workout(url, cat)
                st.success("Added!")
            except:
                st.error("Error")
    
    st.markdown("---")
    try:
        df = utils.get_workouts()
        if not df.empty:
            for i, row in df.iterrows():
                st.markdown(f"**{row['title']}**")
                st.video(row['url'])
    except:
        st.info("No videos yet.")

# --- NAVIGATION MOBILE HORIZONTALE (CORRIGÉE) ---
# Ce bloc est invisible sur PC et s'affiche en bas sur Mobile
st.markdown('<div class="mobile-nav-container">', unsafe_allow_html=True)

# On utilise des colonnes, et le CSS "div[data-testid='column'] { width: 20% !important }" force l'alignement
mob_cols = st.columns(5)

with mob_cols[0]:
    if st.button("🏠", key="m_home", help="Home", use_container_width=True):
        navigate_to("🏠 Home")
with mob_cols[1]:
    if st.button("📅", key="m_cal", help="Calendar", use_container_width=True):
        navigate_to("📅 Workout Calendar")
with mob_cols[2]:
    if st.button("💪", key="m_prog", help="Programs", use_container_width=True):
        navigate_to("💪 Workout Programs")
with mob_cols[3]:
    if st.button("📚", key="m_lib", help="Library", use_container_width=True):
        navigate_to("📚 Exercise Library")
with mob_cols[4]:
    if st.button("🎬", key="m_col", help="Videos", use_container_width=True):
        navigate_to("🎬 My Collection")

st.markdown('</div>', unsafe_allow_html=True)