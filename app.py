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

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Jade Fitness Hub", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. GESTION DE L'ÉTAT (NAVIGATION & HISTORIQUE) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'nav_page' not in st.session_state:
    st.session_state.nav_page = "🏠 Home"
if 'page_history' not in st.session_state:
    st.session_state.page_history = []
# Initialisation sécurisée du calendrier
if 'calendar_month' not in st.session_state:
    st.session_state.calendar_month = datetime.now().month
if 'calendar_year' not in st.session_state:
    st.session_state.calendar_year = datetime.now().year

# Fonction pour naviguer vers une page
def navigate_to(page_name):
    if st.session_state.nav_page != page_name:
        st.session_state.page_history.append(st.session_state.nav_page)
        st.session_state.nav_page = page_name
        st.rerun()

# Fonction pour revenir en arrière
def go_back():
    if st.session_state.page_history:
        previous_page = st.session_state.page_history.pop()
        st.session_state.nav_page = previous_page
        st.rerun()
    else:
        st.session_state.nav_page = "🏠 Home"
        st.rerun()

# --- EXERCISE GIF VIEWER COMPONENT ---
def render_exercise_demo(exercise_name="Exercise", exercise_type="general"):
    """Render an animated GIF demonstration of the exercise"""
    
    # Map exercise types/names to animated GIF URLs from fitness websites
    EXERCISE_GIFS = {
        # Lower Body
        "squats": "https://fitnessprogramer.com/wp-content/uploads/2021/02/SQUAT.gif",
        "squat": "https://fitnessprogramer.com/wp-content/uploads/2021/02/SQUAT.gif",
        "lunges": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lunge.gif",
        "lunge": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lunge.gif",
        "deadlift": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Deadlift.gif",
        "hip_thrust": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Hip-Thrust.gif",
        "glute_bridge": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Glute-Bridge.gif",
        "calf_raise": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Calf-Raise.gif",
        "leg_press": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Leg-Press.gif",
        "leg_curl": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Leg-Curl.gif",
        
        # Upper Body
        "push_up": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-up.gif",
        "push_ups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-up.gif",
        "bench_press": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif",
        "shoulder_press": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Shoulder-Press.gif",
        "bicep_curl": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Curl.gif",
        "tricep_dip": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Triceps-Dip.gif",
        "lateral_raise": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif",
        "row": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Barbell-Row.gif",
        "pull_up": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Pull-up.gif",
        
        # Core
        "plank": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Front-Plank.gif",
        "crunch": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Crunch.gif",
        "sit_up": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Sit-up.gif",
        "leg_raise": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lying-Leg-Raise.gif",
        "russian_twist": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Russian-Twist.gif",
        "mountain_climber": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Mountain-Climber.gif",
        
        # Cardio/HIIT
        "burpee": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Burpee.gif",
        "jumping_jack": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-jack.gif",
        "high_knees": "https://fitnessprogramer.com/wp-content/uploads/2021/02/High-Knee-Run.gif",
        "jump_squat": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jump-Squat.gif",
        "box_jump": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Box-Jump.gif",
        
        # Full Body
        "kettlebell_swing": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Kettlebell-Swing.gif",
        "clean_and_press": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Clean-and-Press.gif",
        
        # Default workout type GIFs
        "lower_body": "https://fitnessprogramer.com/wp-content/uploads/2021/02/SQUAT.gif",
        "upper_body": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-up.gif",
        "core": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Front-Plank.gif",
        "hiit": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Burpee.gif",
        "cardio": "https://fitnessprogramer.com/wp-content/uploads/2021/02/High-Knee-Run.gif",
        "full_body": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Burpee.gif",
        "yoga": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cobra-Stretch.gif",
        "stretching": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Standing-Hamstring-Stretch.gif",
        "pilates": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Crunch.gif",
        
        # Default
        "default": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-jack.gif"
    }
    
    # Get the right GIF for this exercise
    exercise_key = exercise_name.lower().replace(" ", "_").replace("-", "_")
    type_key = exercise_type.lower().replace(" ", "_").replace("-", "_")
    
    # Try exercise name first, then type, then default
    gif_url = EXERCISE_GIFS.get(exercise_key, EXERCISE_GIFS.get(type_key, EXERCISE_GIFS["default"]))
    
    # Render the exercise demo card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0, 30, 60, 0.9) 0%, rgba(0, 60, 90, 0.8) 100%); border-radius: 15px; border: 2px solid rgba(0, 212, 255, 0.3); padding: 15px; box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);">
        <div style="text-align: center; font-family: 'Orbitron', sans-serif; color: #00d4ff; margin-bottom: 10px; font-size: 1.1rem;">🏃‍♀️ {exercise_name}</div>
        <img src="{gif_url}" alt="{exercise_name} demonstration" style="width: 100%; max-height: 300px; object-fit: contain; border-radius: 10px; background: rgba(0,0,0,0.3);">
        <div style="text-align: center; color: #90e0ef; font-size: 0.85rem; margin-top: 10px; font-family: 'Rajdhani', sans-serif;">Watch the form carefully and match the movement</div>
    </div>
    """, unsafe_allow_html=True)

# --- FUTURISTIC BLUE THEME CSS FOR JADE ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Main Background - Deep Space Blue */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #1b263b 100%);
        background-attachment: fixed;
    }
    
    /* Animated Background Particles Effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #00d4ff, transparent),
            radial-gradient(2px 2px at 40px 70px, #00b4d8, transparent),
            radial-gradient(1px 1px at 90px 40px, #48cae4, transparent),
            radial-gradient(2px 2px at 130px 80px, #00d4ff, transparent),
            radial-gradient(1px 1px at 160px 120px, #90e0ef, transparent);
        background-size: 200px 200px;
        animation: sparkle 5s linear infinite;
        pointer-events: none;
        opacity: 0.3;
        z-index: 0;
    }
    
    @keyframes sparkle {
        from { transform: translateY(0); }
        to { transform: translateY(-200px); }
    }
    
    /* Glowing Header */
    .main-header {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00d4ff, #00b4d8, #0077b6, #00d4ff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .sub-header {
        font-family: 'Rajdhani', sans-serif;
        color: #90e0ef;
        text-align: center;
        font-size: 1.2rem;
        letter-spacing: 3px;
        margin-top: 5px;
        opacity: 0.8;
    }
    
    /* Welcome Banner */
    .welcome-banner {
        background: linear-gradient(135deg, rgba(0, 180, 216, 0.1) 0%, rgba(0, 119, 182, 0.2) 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        box-shadow: 
            0 0 20px rgba(0, 212, 255, 0.1),
            inset 0 0 20px rgba(0, 212, 255, 0.05);
    }
    
    .welcome-text {
        font-family: 'Rajdhani', sans-serif;
        color: #caf0f8;
        font-size: 1.3rem;
        margin: 0;
    }
    
    .jade-name {
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
        font-weight: 600;
    }
    
    /* Stats Cards */
    .stats-container {
        display: flex;
        gap: 20px;
        margin: 20px 0;
    }
    
    .stat-card {
        background: linear-gradient(145deg, rgba(0, 119, 182, 0.2), rgba(0, 180, 216, 0.1));
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        flex: 1;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
        border-color: rgba(0, 212, 255, 0.5);
    }
    
    .stat-number {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        color: #00d4ff;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
    
    .stat-label {
        font-family: 'Rajdhani', sans-serif;
        color: #90e0ef;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Workout Cards */
    .workout-card {
        background: linear-gradient(145deg, rgba(13, 27, 42, 0.9), rgba(27, 38, 59, 0.9));
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .workout-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .workout-card:hover::before {
        left: 100%;
    }
    
    .workout-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(0, 212, 255, 0.15),
            0 0 30px rgba(0, 212, 255, 0.1);
        border-color: rgba(0, 212, 255, 0.5);
    }
    
    /* Card Images */
    .stImage img {
        border-radius: 15px;
        border: 2px solid rgba(0, 212, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stImage img:hover {
        border-color: rgba(0, 212, 255, 0.6);
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.3);
    }
    
    /* Text Styling */
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        color: #caf0f8 !important;
    }
    
    h3 {
        font-size: 1rem !important;
        color: #ffffff !important;
        margin: 10px 0 5px 0 !important;
        line-height: 1.3 !important;
    }
    
    p, .stMarkdown {
        font-family: 'Rajdhani', sans-serif;
        color: #90e0ef;
    }
    
    /* Category Badges */
    .category-badge {
        display: inline-block;
        background: linear-gradient(90deg, #0077b6, #00b4d8);
        color: #ffffff;
        padding: 5px 15px;
        border-radius: 20px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 5px 0;
    }
    
    .channel-name {
        color: #48cae4;
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00d4ff !important;
        text-align: center;
    }
    
    /* Sidebar Logo/Avatar Area */
    .sidebar-header {
        text-align: center;
        padding: 20px 0;
        border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        margin-bottom: 20px;
    }
    
    .avatar-ring {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d4ff, #0077b6);
        padding: 4px;
        margin: 0 auto 15px auto;
        animation: pulse-ring 2s ease-in-out infinite;
    }
    
    @keyframes pulse-ring {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.4); }
        50% { box-shadow: 0 0 40px rgba(0, 212, 255, 0.8); }
    }
    
    .avatar-inner {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: linear-gradient(135deg, #1b263b, #0d1b2a);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
    }
    
    .sidebar-name {
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
        font-size: 1.5rem;
        margin: 10px 0 5px 0;
    }
    
    .sidebar-tagline {
        font-family: 'Rajdhani', sans-serif;
        color: #90e0ef;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea {
        background: rgba(0, 119, 182, 0.1) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #caf0f8 !important;
        font-family: 'Rajdhani', sans-serif !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #48cae4 !important;
        opacity: 0.6 !important;
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        background: rgba(0, 119, 182, 0.1) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #caf0f8 !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: rgba(0, 119, 182, 0.05);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stRadio label {
        color: #90e0ef !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 20px rgba(0, 180, 216, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00b4d8, #48cae4) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Video Player Styling */
    .stVideo {
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid rgba(0, 212, 255, 0.3);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.1), rgba(72, 202, 228, 0.1)) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stError {
        background: linear-gradient(90deg, rgba(255, 107, 107, 0.1), rgba(238, 82, 83, 0.1)) !important;
        border: 1px solid rgba(255, 107, 107, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* Info Box */
    .stInfo {
        background: linear-gradient(90deg, rgba(0, 180, 216, 0.1), rgba(0, 119, 182, 0.1)) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #caf0f8 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #00d4ff !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d1b2a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0077b6, #00b4d8);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00b4d8, #48cae4);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Section Dividers */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
        margin: 30px 0;
        border: none;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0, 119, 182, 0.1);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #90e0ef;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
        color: white !important;
    }
    
    /* Calendar Styles */
    .calendar-container {
        background: linear-gradient(145deg, rgba(13, 27, 42, 0.9), rgba(27, 38, 59, 0.9));
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .calendar-day {
        background: rgba(0, 119, 182, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        min-height: 80px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .calendar-day:hover {
        background: rgba(0, 180, 216, 0.2);
        border-color: rgba(0, 212, 255, 0.5);
        transform: scale(1.05);
    }
    
    .calendar-day.today {
        background: linear-gradient(135deg, rgba(0, 180, 216, 0.3), rgba(0, 119, 182, 0.3));
        border-color: #00d4ff;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }
    
    .calendar-day.has-workout {
        border-color: #00d4ff;
        background: rgba(0, 212, 255, 0.1);
    }
    
    .calendar-day-num {
        font-family: 'Orbitron', sans-serif;
        color: #caf0f8;
        font-size: 1.2rem;
    }
    
    .calendar-workout-indicator {
        width: 8px;
        height: 8px;
        background: #00d4ff;
        border-radius: 50%;
        display: inline-block;
        margin: 2px;
        box-shadow: 0 0 5px #00d4ff;
    }
    
    /* Program Cards */
    .program-card {
        background: linear-gradient(145deg, rgba(13, 27, 42, 0.95), rgba(27, 38, 59, 0.95));
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        transition: all 0.4s ease;
    }
    
    .program-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 212, 255, 0.2);
        border-color: rgba(0, 212, 255, 0.5);
    }
    
    .program-title {
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
        font-size: 1.5rem;
        margin-bottom: 10px;
    }
    
    .program-meta {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        margin: 15px 0;
    }
    
    .program-tag {
        background: rgba(0, 119, 182, 0.3);
        color: #90e0ef;
        padding: 5px 12px;
        border-radius: 15px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.85rem;
    }
    
    /* Exercise Table */
    .exercise-row {
        background: rgba(0, 119, 182, 0.1);
        border-radius: 10px;
        padding: 12px 15px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid #00d4ff;
    }
    
    .exercise-name {
        font-family: 'Rajdhani', sans-serif;
        color: #caf0f8;
        font-weight: 600;
    }
    
    .exercise-details {
        color: #90e0ef;
        font-size: 0.9rem;
    }
    
    /* Motivational Quote */
    .quote-box {
        background: linear-gradient(135deg, rgba(0, 180, 216, 0.05), rgba(0, 119, 182, 0.1));
        border-left: 4px solid #00d4ff;
        padding: 15px 20px;
        margin: 20px 0;
        border-radius: 0 15px 15px 0;
        font-style: italic;
    }
    
    .quote-text {
        font-family: 'Rajdhani', sans-serif;
        color: #caf0f8;
        font-size: 1.1rem;
        margin: 0;
    }
    
    .quote-author {
        color: #48cae4;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    
    /* Date Input */
    .stDateInput > div > div {
        background: rgba(0, 119, 182, 0.1) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #90e0ef !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(0, 119, 182, 0.1) !important;
        border-radius: 10px !important;
        color: #caf0f8 !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Action Cards */
    .action-card {
        background: linear-gradient(145deg, rgba(13, 27, 42, 0.9), rgba(27, 38, 59, 0.9));
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .action-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 212, 255, 0.2);
        border-color: #00d4ff;
    }
    
    /* ===== VISUALIZATION STYLES ===== */
    
    /* Progress Ring */
    .progress-ring-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 20px 0;
    }
    
    .progress-ring {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(
            #00d4ff var(--progress, 0%),
            rgba(0, 119, 182, 0.2) var(--progress, 0%)
        );
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .progress-ring::before {
        content: '';
        position: absolute;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: #0d1b2a;
    }
    
    .progress-value {
        position: relative;
        z-index: 1;
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    /* Muscle Group Chart */
    .muscle-chart {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding: 20px;
        background: rgba(0, 119, 182, 0.05);
        border-radius: 15px;
    }
    
    .muscle-bar-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .muscle-label {
        min-width: 80px;
        font-family: 'Rajdhani', sans-serif;
        color: #90e0ef;
        font-size: 0.9rem;
    }
    
    .muscle-bar-bg {
        flex: 1;
        height: 20px;
        background: rgba(0, 119, 182, 0.2);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .muscle-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #0077b6, #00d4ff);
        border-radius: 10px;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    .muscle-percent {
        min-width: 40px;
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
        font-size: 0.85rem;
        text-align: right;
    }
    
    /* Weekly Schedule Visual */
    .week-visual {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        margin: 20px 0;
        padding: 15px;
        background: rgba(0, 119, 182, 0.05);
        border-radius: 15px;
    }
    
    .day-circle {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 0.75rem;
        border: 2px solid rgba(0, 212, 255, 0.3);
        background: rgba(0, 119, 182, 0.1);
        color: #90e0ef;
        transition: all 0.3s ease;
    }
    
    .day-circle.active {
        background: linear-gradient(135deg, #0077b6, #00d4ff);
        border-color: #00d4ff;
        color: white;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }
    
    .day-circle.rest {
        background: rgba(144, 224, 239, 0.1);
        border-color: rgba(144, 224, 239, 0.3);
        color: #48cae4;
    }
    
    /* Intensity Meter */
    .intensity-meter {
        display: flex;
        gap: 4px;
        margin: 10px 0;
    }
    
    .intensity-bar {
        width: 20px;
        height: 30px;
        border-radius: 5px;
        background: rgba(0, 119, 182, 0.2);
        transition: all 0.3s ease;
    }
    
    .intensity-bar.filled {
        background: linear-gradient(180deg, #00d4ff, #0077b6);
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    .intensity-bar.filled.high {
        background: linear-gradient(180deg, #ff6b6b, #ee5253);
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .mini-stat {
        background: linear-gradient(145deg, rgba(13, 27, 42, 0.9), rgba(27, 38, 59, 0.9));
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
    }
    
    .mini-stat-icon {
        font-size: 1.5rem;
        margin-bottom: 5px;
    }
    
    .mini-stat-value {
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .mini-stat-label {
        font-family: 'Rajdhani', sans-serif;
        color: #90e0ef;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ===== MOBILE RESPONSIVE STYLES ===== */
    
    /* iPhone and small screens */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem !important;
        }
        
        .sub-header {
            font-size: 0.9rem !important;
            letter-spacing: 1px !important;
        }
        
        .stat-card {
            padding: 15px 10px !important;
            margin: 5px !important;
        }
        
        .stat-number {
            font-size: 1.8rem !important;
        }
        
        .stat-label {
            font-size: 0.7rem !important;
        }
        
        .workout-card {
            padding: 15px !important;
            margin: 10px 5px !important;
        }
        
        .program-card {
            padding: 15px !important;
            margin: 10px 0 !important;
        }
        
        .program-title {
            font-size: 1.2rem !important;
        }
        
        .program-meta {
            gap: 8px !important;
        }
        
        .program-tag {
            padding: 4px 8px !important;
            font-size: 0.75rem !important;
        }
        
        .welcome-banner {
            padding: 15px !important;
            margin: 10px 0 !important;
        }
        
        .action-card {
            padding: 20px 15px !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.2rem !important;
        }
        
        h3 {
            font-size: 0.95rem !important;
        }
        
        .stButton > button {
            padding: 10px 20px !important;
            font-size: 0.85rem !important;
        }
        
        /* Sidebar mobile */
        section[data-testid="stSidebar"] {
            min-width: 250px !important;
        }
        
        .avatar-ring {
            width: 70px !important;
            height: 70px !important;
        }
        
        .sidebar-name {
            font-size: 1.2rem !important;
        }
        
        .nav-item {
            padding: 12px 15px !important;
            font-size: 0.9rem !important;
        }
        
        /* Calendar mobile */
        .calendar-day {
            min-height: 50px !important;
            padding: 5px !important;
            margin: 2px !important;
        }
        
        .calendar-day-num {
            font-size: 0.9rem !important;
        }
        
        /* Exercise rows mobile */
        .exercise-row {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 5px !important;
            padding: 10px !important;
        }
        
        /* Week visual mobile */
        .week-visual {
            gap: 4px !important;
            padding: 10px !important;
        }
        
        .day-circle {
            width: 35px !important;
            height: 35px !important;
            font-size: 0.65rem !important;
        }
        
        /* Stats grid mobile */
        .stats-grid {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 10px !important;
        }
        
        /* Muscle chart mobile */
        .muscle-label {
            min-width: 60px !important;
            font-size: 0.8rem !important;
        }
        
        .muscle-bar-bg {
            height: 15px !important;
        }
    }
    
    /* Extra small screens (iPhone SE, etc.) */
    @media (max-width: 375px) {
        .main-header {
            font-size: 1.5rem !important;
        }
        
        .stat-card {
            padding: 10px 8px !important;
        }
        
        .stat-number {
            font-size: 1.5rem !important;
        }
        
        .day-circle {
            width: 30px !important;
            height: 30px !important;
            font-size: 0.6rem !important;
        }
        
        .stats-grid {
            grid-template-columns: 1fr 1fr !important;
        }
    }
    
    /* Tablet portrait */
    @media (min-width: 768px) and (max-width: 1024px) {
        .stat-card {
            padding: 20px !important;
        }
        
        .workout-card {
            padding: 20px !important;
        }
    }
    
    /* ===== STREAK SYSTEM STYLES ===== */
    .streak-container {
        background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(255, 165, 0, 0.1));
        border: 2px solid rgba(255, 165, 0, 0.4);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin: 15px 0;
        position: relative;
        overflow: hidden;
    }
    
    .streak-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 165, 0, 0.1) 0%, transparent 70%);
        animation: pulse-glow 2s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
    }
    
    .streak-flames {
        font-size: 2.5rem;
        margin-bottom: 5px;
        animation: flame-dance 0.5s ease-in-out infinite alternate;
    }
    
    @keyframes flame-dance {
        from { transform: translateY(0) scale(1); }
        to { transform: translateY(-3px) scale(1.05); }
    }
    
    .streak-number {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #ffa500;
        text-shadow: 0 0 20px rgba(255, 165, 0, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .streak-label {
        font-family: 'Rajdhani', sans-serif;
        color: #ffcc80;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .streak-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ffa500, #ff6b00);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        margin-top: 10px;
        box-shadow: 0 0 15px rgba(255, 165, 0, 0.4);
    }
    
    /* Calendar streak day styles */
    .calendar-day.streak-day {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(255, 107, 0, 0.1)) !important;
        border-color: #ffa500 !important;
        box-shadow: 0 0 10px rgba(255, 165, 0, 0.3);
    }
    
    .calendar-day.completed-day {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 200, 100, 0.1)) !important;
        border-color: #00ff88 !important;
    }
    
    .calendar-day.missed-day {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(200, 50, 50, 0.1)) !important;
        border-color: rgba(255, 107, 107, 0.5) !important;
    }
    
    .day-flame {
        position: absolute;
        top: 2px;
        right: 2px;
        font-size: 0.8rem;
    }
    
    /* Confirm Complete Button */
    .confirm-btn {
        background: linear-gradient(135deg, #00ff88, #00cc6a) !important;
        color: #0a0a1a !important;
        font-weight: 700 !important;
        padding: 15px 30px !important;
        font-size: 1.1rem !important;
        border-radius: 30px !important;
        box-shadow: 0 5px 25px rgba(0, 255, 136, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .confirm-btn:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 35px rgba(0, 255, 136, 0.5) !important;
    }
    
    /* ===== PERFORMANCE OPTIMIZATIONS ===== */
    * {
        -webkit-tap-highlight-color: transparent;
        touch-action: manipulation;
    }
    
    /* Hardware acceleration for animations */
    .mobile-nav-item, .stButton > button, .program-card, .workout-card, .action-card {
        will-change: transform;
        transform: translateZ(0);
        -webkit-transform: translateZ(0);
    }
    
    /* Reduce motion for users who prefer it */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* ===== ENHANCED MOBILE STYLES ===== */
    @media (max-width: 768px) {
        /* Show horizontal bottom nav, hide sidebar completely */
        .mobile-nav {
            display: block !important;
        }
        
        section[data-testid="stSidebar"] {
            display: none !important;
            width: 0 !important;
            min-width: 0 !important;
        }
        
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Add bottom padding for content above nav */
        .main .block-container {
            padding-bottom: 90px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Full width content */
        .main {
            margin-left: 0 !important;
        }
        
        /* Larger touch targets */
        .stButton > button {
            min-height: 48px !important;
            padding: 12px 24px !important;
            font-size: 1rem !important;
        }
        
        /* Faster animations on mobile */
        .program-card, .workout-card, .action-card {
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }
        
        /* Optimize images */
        img {
            content-visibility: auto;
        }
        
        /* Streak container mobile */
        .streak-container {
            padding: 15px;
            margin: 10px 0;
        }
        
        .streak-number {
            font-size: 2.5rem;
        }
        
        .streak-flames {
            font-size: 2rem;
        }
    }
    
    /* iOS safe areas */
    @supports (padding: max(0px)) {
        .mobile-nav {
            padding-bottom: max(8px, env(safe-area-inset-bottom));
        }
        
        .main .block-container {
            padding-bottom: max(100px, calc(80px + env(safe-area-inset-bottom))) !important;
        }
    }
    
    /* ===== LOGIN PAGE STYLES ===== */
    .login-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: linear-gradient(135deg, rgba(0, 30, 60, 0.9) 0%, rgba(0, 60, 100, 0.8) 100%);
        border-radius: 30px;
        border: 2px solid rgba(0, 212, 255, 0.4);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(0, 212, 255, 0.2);
        backdrop-filter: blur(20px);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .login-avatar {
        width: 120px;
        height: 120px;
        margin: 0 auto 20px;
        background: linear-gradient(135deg, #00d4ff, #0077b6);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.5);
        animation: pulse-avatar 2s ease-in-out infinite;
    }
    
    @keyframes pulse-avatar {
        0%, 100% { box-shadow: 0 0 40px rgba(0, 212, 255, 0.5); }
        50% { box-shadow: 0 0 60px rgba(0, 212, 255, 0.8); }
    }
    
    .login-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        background: linear-gradient(90deg, #00d4ff, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .login-subtitle {
        font-family: 'Rajdhani', sans-serif;
        color: #90e0ef;
        font-size: 1rem;
        letter-spacing: 2px;
    }
    
    .welcome-features {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin: 30px 0;
    }
    
    .feature-item {
        background: rgba(0, 119, 182, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 5px;
    }
    
    .feature-text {
        font-family: 'Rajdhani', sans-serif;
        color: #caf0f8;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIN/AUTHENTICATION SYSTEM ---
def show_login_page():
    """Display the login page"""
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <div class="login-avatar">💎</div>
            <div class="login-title">JADE FITNESS</div>
            <div class="login-subtitle">YOUR TRANSFORMATION STARTS HERE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 👋 Welcome, Jade!")
        st.markdown("*Your personal fitness sanctuary awaits*")
        
        # Features showcase
        st.markdown("""
        <div class="welcome-features">
            <div class="feature-item">
                <div class="feature-icon">💪</div>
                <div class="feature-text">Workout Programs</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">📅</div>
                <div class="feature-text">Smart Calendar</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🔥</div>
                <div class="feature-text">Streak Tracking</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🎮</div>
                <div class="feature-text">3D Exercises</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple PIN or password entry
        st.markdown("---")
        password = st.text_input("🔐 Enter your PIN (default: 1234)", type="password", key="login_pin")
        
        if st.button("✨ Enter My Fitness Hub", use_container_width=True, type="primary"):
            if password == "1234" or password == "jade" or password == "":
                st.session_state.logged_in = True
                st.session_state.user_name = "Jade"
                # Initialize calendar and populate with sample workouts if empty
                try:
                    utils.init_calendar()
                    utils.populate_sample_workouts()
                except:
                    pass
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Incorrect PIN")

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Show login page if not logged in
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    # Jade's Profile Section
    st.markdown("""
    <div class="sidebar-header">
        <div class="avatar-ring">
            <div class="avatar-inner">💎</div>
        </div>
        <div class="sidebar-name">JADE</div>
        <div class="sidebar-tagline">✨ Fitness Queen ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Greeting based on time
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
        emoji = "🌅"
    elif hour < 17:
        greeting = "Good Afternoon"
        emoji = "☀️"
    else:
        greeting = "Good Evening"
        emoji = "🌙"
    
    st.markdown(f"### {emoji} {greeting}, Jade!")
    
    st.markdown("---")
    
    # Navigation - with session state support for quick action buttons
    st.markdown("## 🧭 Navigation")
    
    nav_options = ["🏠 Home", "📅 Workout Calendar", "💪 Workout Programs", "📚 Exercise Library", "🎬 My Collection"]
    
    # On trouve l'index actuel
    current_index = 0
    if st.session_state.nav_page in nav_options:
        current_index = nav_options.index(st.session_state.nav_page)
        
    selected = st.radio("Menu", nav_options, index=current_index, label_visibility="collapsed")
    
    if selected != st.session_state.nav_page:
        navigate_to(selected)
    
    st.markdown("---")
    
    # Quick Stats in Sidebar
    try:
        df_sidebar = utils.get_workouts()
        total_workouts = len(df_sidebar)
        calendar_data = utils.load_calendar()
        scheduled_days = len(calendar_data)
    except:
        total_workouts = 0
        scheduled_days = 0
    
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background: rgba(0, 119, 182, 0.1); border-radius: 10px; border: 1px solid rgba(0, 212, 255, 0.2);">
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: #00d4ff;">{total_workouts}</div>
            <div style="font-family: 'Rajdhani', sans-serif; color: #90e0ef; font-size: 0.7rem;">VIDEOS</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background: rgba(0, 119, 182, 0.1); border-radius: 10px; border: 1px solid rgba(0, 212, 255, 0.2);">
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: #00d4ff;">{scheduled_days}</div>
            <div style="font-family: 'Rajdhani', sans-serif; color: #90e0ef; font-size: 0.7rem;">SCHEDULED</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Streak display in sidebar
    try:
        streak_data = utils.get_streak_data()
    except:
        streak_data = {'current_streak': 0}
        
    st.markdown("### 🔥 Current Streak")
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(255, 165, 0, 0.1)); border-radius: 15px; border: 2px solid rgba(255, 165, 0, 0.4);">
        <div style="font-size: 2rem;">{'🔥' * min(streak_data['current_streak'], 5) if streak_data['current_streak'] > 0 else '💪'}</div>
        <div style="font-family: 'Orbitron', sans-serif; font-size: 2rem; color: #ffa500;">{streak_data['current_streak']}</div>
        <div style="font-family: 'Rajdhani', sans-serif; color: #ffcc80; font-size: 0.8rem;">DAY STREAK</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.nav_page = "🏠 Home"
        st.rerun()

# --- MAIN CONTENT ---
page = st.session_state.nav_page

# --- BACK BUTTON (Top of page, not on Home) ---
if page != "🏠 Home":
    if st.button("⬅️ Retour", key="top_back_btn"):
        go_back()

# ===== HOME PAGE =====
if page == "🏠 Home":
    # Header
    st.markdown('<h1 class="main-header">💎 JADE FITNESS HUB 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">YOUR PERSONAL WORKOUT SANCTUARY</p>', unsafe_allow_html=True)
    
    # Welcome Banner with Quote
    quotes = [
        ("The only bad workout is the one that didn't happen.", "Unknown"),
        ("Strong is the new beautiful.", "Unknown"),
        ("Your body can stand almost anything. It's your mind you have to convince.", "Unknown")
    ]
    quote, author = random.choice(quotes)
    st.markdown(f"""
    <div class="welcome-banner">
        <p class="welcome-text">Welcome back, <span class="jade-name">Jade</span>! Ready to crush your goals today? 💪</p>
        <div class="quote-box">
            <p class="quote-text">"{quote}"</p>
            <p class="quote-author">— {author}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🔥 STREAK DISPLAY
    try:
        streak_data = utils.get_streak_data()
        current_streak = streak_data['current_streak']
        best_streak = streak_data['best_streak']
        streak_status = streak_data['streak_status']
    except:
        current_streak = 0
        best_streak = 0
        streak_status = 'normal'
    
    # Determine streak message and flame animation
    if current_streak >= 7:
        flame_emoji = "🔥🔥🔥"
        streak_badge = "UNSTOPPABLE!"
    elif current_streak >= 3:
        flame_emoji = "🔥🔥"
        streak_badge = "ON FIRE!"
    elif current_streak >= 1:
        flame_emoji = "🔥"
        streak_badge = "KEEP GOING!"
    else:
        flame_emoji = "💪"
        streak_badge = "START TODAY!"
    
    col_streak1, col_streak2 = st.columns([2, 1])
    
    with col_streak1:
        st.markdown(f"""
        <div class="streak-container">
            <div class="streak-flames">{flame_emoji}</div>
            <div class="streak-number">{current_streak}</div>
            <div class="streak-label">DAY STREAK</div>
            <div class="streak-badge">{streak_badge}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_streak2:
        st.markdown(f"""
        <div style="background: rgba(0, 119, 182, 0.1); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 15px; padding: 15px; text-align: center; height: 100%;">
            <div style="margin-bottom: 15px;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.8rem; color: #00d4ff;">🏆 {best_streak}</div>
                <div style="font-family: 'Rajdhani', sans-serif; color: #90e0ef; font-size: 0.75rem; text-transform: uppercase;">Best Streak</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("## ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">📅</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Plan Workout</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📅 Go to Calendar", key="nav_calendar", use_container_width=True):
            navigate_to("📅 Workout Calendar")
        
    with col2:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">💪</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Browse Programs</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💪 View Programs", key="nav_programs", use_container_width=True):
            navigate_to("💪 Workout Programs")
        
    with col3:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎬</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Watch Videos</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎬 My Collection", key="nav_collection", use_container_width=True):
            navigate_to("🎬 My Collection")

# ===== CALENDAR PAGE =====
elif page == "📅 Workout Calendar":
    st.markdown('<h1 class="main-header">📅 WORKOUT CALENDAR</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">YOUR ONE-YEAR FITNESS JOURNEY</p>', unsafe_allow_html=True)
    
    # Initialize calendar safely
    try:
        utils.init_calendar()
        calendar_data = utils.load_calendar()
    except:
        calendar_data = {}
    
    # Calendar Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀️ Previous Month"):
            if st.session_state.calendar_month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year -= 1
            else:
                st.session_state.calendar_month -= 1
            st.rerun()
    
    with col2:
        month_name = calendar.month_name[st.session_state.calendar_month]
        st.markdown(f"""
        <h2 style="text-align: center; color: #00d4ff; font-family: 'Orbitron', sans-serif;">
            {month_name} {st.session_state.calendar_year}
        </h2>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("Next Month ▶️"):
            if st.session_state.calendar_month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year += 1
            else:
                st.session_state.calendar_month += 1
            st.rerun()
    
    # Calendar Grid
    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    month_days = cal.monthdayscalendar(st.session_state.calendar_year, st.session_state.calendar_month)
    today = datetime.now()
    days = ["S", "M", "T", "W", "T", "F", "S"]
    
    calendar_html = """
    <style>
        .cal-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 4px;
            margin: 10px 0;
        }
        .cal-header {
            text-align: center;
            padding: 8px 4px;
            color: #00d4ff;
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            font-size: 0.8rem;
            background: rgba(0, 119, 182, 0.2);
            border-radius: 5px;
        }
        .cal-day {
            text-align: center;
            padding: 8px 4px;
            min-height: 50px;
            border-radius: 8px;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .cal-day-num {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            font-weight: 500;
        }
        .cal-day-icon {
            font-size: 0.8rem;
            margin-top: 2px;
        }
        .cal-day-empty { background: transparent; }
        .cal-day-normal {
            background: rgba(0, 119, 182, 0.1);
            border: 1px solid rgba(0, 212, 255, 0.2);
            color: #caf0f8;
        }
        .cal-day-workout {
            background: rgba(0, 212, 255, 0.15);
            border: 2px solid rgba(0, 212, 255, 0.5);
            color: #90e0ef;
        }
        .cal-day-today {
            background: rgba(0, 180, 216, 0.3);
            border: 2px solid #00d4ff;
            color: #00d4ff;
            font-weight: 700;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        }
    </style>
    <div class="cal-grid">
    """
    
    # Add day headers
    for day in days:
        calendar_html += f'<div class="cal-header">{day}</div>'
    
    # Add calendar days
    for week in month_days:
        for day in week:
            if day == 0:
                calendar_html += '<div class="cal-day cal-day-empty"></div>'
            else:
                date_str = f"{st.session_state.calendar_year}-{st.session_state.calendar_month:02d}-{day:02d}"
                is_today = (day == today.day and 
                            st.session_state.calendar_month == today.month and 
                            st.session_state.calendar_year == today.year)
                has_workouts = date_str in calendar_data and len(calendar_data[date_str]) > 0
                
                if is_today:
                    css_class = "cal-day-today"
                    icon = "⭐" if has_workouts else "📍"
                elif has_workouts:
                    css_class = "cal-day-workout"
                    icon = "💪"
                else:
                    css_class = "cal-day-normal"
                    icon = ""
                
                calendar_html += f'''
                <div class="cal-day {css_class}">
                    <div class="cal-day-num">{day}</div>
                    <div class="cal-day-icon">{icon}</div>
                </div>
                '''
    
    calendar_html += '</div>'
    st.markdown(calendar_html, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Add/Edit Workout for a Date
    st.markdown("## ➕ Schedule a Workout")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_date = st.date_input("📅 Select Date", datetime.now())
        workout_name = st.text_input("💪 Workout Name", placeholder="e.g., Morning HIIT Session")
        workout_type = st.selectbox("🏋️ Workout Type", 
            ["Strength", "Cardio", "HIIT", "Yoga", "Pilates", "Dance", "Stretching", "Full Body", "Upper Body", "Lower Body", "Core"])
    
    with col2:
        workout_duration = st.selectbox("⏱️ Duration", 
            ["15 min", "20 min", "30 min", "45 min", "60 min", "90 min"])
        workout_notes = st.text_area("📝 Notes (optional)", placeholder="Any notes for this workout...")
        
    if st.button("✨ Add to Calendar", use_container_width=True):
        if workout_name:
            date_str = selected_date.strftime("%Y-%m-%d")
            workout_data = {
                "name": workout_name,
                "type": workout_type,
                "duration": workout_duration,
                "notes": workout_notes,
                "completed": False
            }
            try:
                utils.add_workout_to_calendar(date_str, workout_data)
                st.success(f"🎉 Workout added for {selected_date.strftime('%B %d, %Y')}!")
                st.rerun()
            except:
                st.error("Error saving workout. Please try again.")
        else:
            st.warning("⚠️ Please enter a workout name!")

# ===== WORKOUT PROGRAMS PAGE =====
elif page == "💪 Workout Programs":
    st.markdown('<h1 class="main-header">💪 WORKOUT PROGRAMS</h1>', unsafe_allow_html=True)
    
    try:
        programs = utils.get_workout_programs()
    except:
        programs = {}
    
    # Program Selection
    if 'selected_program' not in st.session_state:
        st.session_state.selected_program = None
    
    # Show program list if no program selected
    if st.session_state.selected_program is None:
        st.markdown("## 🎯 Choose Your Program")
        
        for program_id, program in programs.items():
            with st.container():
                st.markdown(f"""
                <div class="program-card" style="margin-bottom: 15px;">
                    <div class="program-title">{program['name']}</div>
                    <p style="color: #caf0f8; font-family: 'Rajdhani', sans-serif; margin: 10px 0;">{program['description']}</p>
                    <div class="program-meta">
                        <span class="program-tag">📅 {program['duration']}</span>
                        <span class="program-tag">📊 {program['level']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📖 View Details & Schedule", key=f"view_{program_id}", use_container_width=True):
                    st.session_state.selected_program = program_id
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    # Show selected program details
    else:
        selected = programs[st.session_state.selected_program]
        
        st.markdown(f"## 📋 {selected['name']}")
        st.markdown(f"*{selected['description']}*")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        st.markdown("### 📋 Detailed Schedule")
        
        if 'phases' in selected:
            for phase_name, phase_data in selected['phases'].items():
                st.markdown(f"## 🚀 {phase_name}")
                st.markdown(f"**Focus:** {phase_data['focus']}")
                st.markdown("---")
        elif 'schedule' in selected:
            for week_name, week_schedule in selected['schedule'].items():
                st.markdown(f"### 📅 {week_name}")
                for day_name, day_data in week_schedule.items():
                    with st.expander(f"**{day_name}** - {day_data['focus']}", expanded=False):
                        st.markdown(f"**🎯 Focus:** {day_data['focus']}")
                        st.markdown("---")
                        for exercise in day_data['exercises']:
                            st.markdown(f"- {exercise['name']} ({exercise['sets']} sets x {exercise['reps']})")

# ===== EXERCISE LIBRARY PAGE =====
elif page == "📚 Exercise Library":
    st.markdown('<h1 class="main-header">📚 EXERCISE LIBRARY</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">LEARN PROPER FORM WITH GIF DEMONSTRATIONS</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search exercises", placeholder="Search by name or muscle group...")
    with col2:
        category_filter = st.selectbox("📂 Category", EXERCISE_CATEGORIES)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    if search_query:
        exercises = search_exercises(search_query)
    else:
        exercises = EXERCISE_LIBRARY.copy()
    
    if category_filter != "All":
        exercises = {k: v for k, v in exercises.items() if v["category"] == category_filter}
    
    st.markdown(f"### 💪 {len(exercises)} Exercises Found")
    
    if 'selected_exercise' not in st.session_state:
        st.session_state.selected_exercise = None
    
    if st.session_state.selected_exercise is None:
        exercise_list = list(exercises.items())
        for i in range(0, len(exercise_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(exercise_list):
                    key, exercise = exercise_list[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="program-card" style="text-align: center; min-height: 200px;">
                            <div class="program-title" style="font-size: 1.1rem;">{exercise['name']}</div>
                            <span class="program-tag">{exercise['category']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"📖 View Exercise", key=f"view_ex_{key}", use_container_width=True):
                            st.session_state.selected_exercise = key
                            st.rerun()
    else:
        exercise = EXERCISE_LIBRARY[st.session_state.selected_exercise]
        st.markdown(f"## {exercise['name']}")
        
        render_exercise_demo(
            exercise_name=exercise['name'],
            exercise_type=exercise.get('category', 'general')
        )
        
        tab1, tab2 = st.tabs(["📋 Instructions", "⚠️ Mistakes"])
        with tab1:
            st.markdown("### Step-by-Step Execution")
            for i, step in enumerate(exercise['instructions']['execution'], 1):
                st.write(f"{i}. {step}")
        with tab2:
            st.markdown("### Common Mistakes")
            for mistake in exercise['instructions']['common_mistakes']:
                st.warning(f"⚠️ {mistake}")

# ===== MY COLLECTION PAGE =====
elif page == "🎬 My Collection":
    st.markdown('<h1 class="main-header">🎬 MY COLLECTION</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">YOUR SAVED WORKOUT VIDEOS</p>', unsafe_allow_html=True)
    
    st.markdown("## ➕ Add New Video")
    col1, col2 = st.columns([2, 1])
    with col1:
        url_input = st.text_input("🔗 YouTube URL", placeholder="Paste video link here...")
    with col2:
        category_input = st.selectbox("📂 Category", ["💪 Strength", "❤️ Cardio", "🧘 Yoga", "💃 Dance"])
    
    if st.button("✨ Add to Collection", use_container_width=True):
        if url_input:
            success = utils.add_workout(url_input, category_input)
            if success:
                st.success("🎉 Workout added successfully!")
                st.rerun()
            else:
                st.error("❌ Couldn't find the video.")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    try:
        df = utils.get_workouts()
        if not df.empty:
            for i in range(0, len(df), 3):
                cols = st.columns(3, gap="medium")
                for j in range(3):
                    if i + j < len(df):
                        row = df.iloc[i + j]
                        with cols[j]:
                            st.markdown('<div class="workout-card">', unsafe_allow_html=True)
                            st.image(row['thumbnail'], use_container_width=True)
                            st.markdown(f"### {row['title']}")
                            if st.button(f"▶️ Watch Now", key=f"btn_{i+j}", use_container_width=True):
                                st.video(row['url'])
                            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No workouts added yet.")
    except:
        st.error("Could not load collection.")

# Footer
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 20px; opacity: 0.7;">
    <p style="font-family: 'Rajdhani', sans-serif; color: #48cae4; font-size: 0.9rem;">
        Made with 💙 for Jade | Stay Strong, Stay Beautiful ✨
    </p>
</div>
""", unsafe_allow_html=True)

# --- FIXED MOBILE NAVIGATION (Native Streamlit Buttons with CSS fix) ---
st.markdown("""
<style>
    /* Default hidden on PC */
    .mobile-nav-container { display: none; }

    /* Only visible on mobile */
    @media (max-width: 768px) {
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
        /* CRUCIAL FIX: Force columns to stay in a row */
        div[data-testid="column"] {
            width: 20% !important;
            flex: 1 1 auto !important;
            min-width: 50px !important;
        }
        .stButton button {
            width: 100%;
            padding: 0.5rem 0;
            font-size: 1.5rem;
            line-height: 1;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="mobile-nav-container">', unsafe_allow_html=True)
mob_col1, mob_col2, mob_col3, mob_col4, mob_col5 = st.columns(5)

with mob_col1:
    if st.button("🏠", key="mob_home", help="Home", use_container_width=True):
        navigate_to("🏠 Home")
with mob_col2:
    if st.button("📅", key="mob_cal", help="Calendar", use_container_width=True):
        navigate_to("📅 Workout Calendar")
with mob_col3:
    if st.button("💪", key="mob_prog", help="Programs", use_container_width=True):
        navigate_to("💪 Workout Programs")
with mob_col4:
    if st.button("📚", key="mob_lib", help="Library", use_container_width=True):
        navigate_to("📚 Exercise Library")
with mob_col5:
    if st.button("🎬", key="mob_col", help="Collection", use_container_width=True):
        navigate_to("🎬 My Collection")
st.markdown('</div>', unsafe_allow_html=True)