import streamlit as st
import utils
import pandas as pd
from datetime import datetime, timedelta
import calendar
import random
from streamlit_calendar import calendar as st_calendar
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

# --- BACK BUTTON STATE MANAGEMENT ---
# Initialize page history in session state if it doesn't exist
# --- NAVIGATION WITH QUERY PARAMS (for native back gesture support) ---
PAGE_MAPPING = {
    'home': '🏠 Home',
    'calendar': '📅 Workout Calendar',
    'programs': '💪 Workout Programs',
    'library': '📚 Exercise Library',
    'collection': '🎬 My Collection'
}

PAGE_REVERSE_MAPPING = {v: k for k, v in PAGE_MAPPING.items()}

def get_current_page_from_url():
    """Read page from URL query params"""
    params = st.query_params
    page_key = params.get('page', 'home')
    return PAGE_MAPPING.get(page_key, '🏠 Home')

def navigate_to(page_name):
    """Navigate to a new page using query params (creates browser history)"""
    page_key = PAGE_REVERSE_MAPPING.get(page_name, 'home')
    st.query_params['page'] = page_key
    st.rerun()

def go_back():
    """Go back to home page"""
    navigate_to('🏠 Home')
    pass

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
    .cal-grid { 
        display: grid; 
        grid-template-columns: repeat(7, 1fr); 
        gap: 5px; 
        margin: 10px 0; 
    }
    .cal-header { 
        text-align: center; 
        padding: 5px; 
        color: #00d4ff; 
        font-family: 'Orbitron', sans-serif; 
        font-size: 0.8rem; 
        font-weight: bold;
    }
    .cal-day { 
        text-align: center; 
        padding: 5px; 
        min-height: 60px; 
        border-radius: 10px; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        font-size: 0.9rem;
    }
    .cal-day-normal { 
        background: rgba(0, 119, 182, 0.1); 
        border: 1px solid rgba(0, 212, 255, 0.1); 
        color: #caf0f8; 
    }
    .cal-day-today { 
        background: rgba(0, 180, 216, 0.3); 
        border: 2px solid #00d4ff; 
        color: #ffffff; 
        font-weight: bold; 
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    .cal-day-workout { 
        background: rgba(0, 255, 136, 0.1); 
        border: 1px solid #00ff88; 
        color: #00ff88; 
    }
    .cal-icon { font-size: 1rem; margin-top: 2px; }
    
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
    /* Mobile nav styles are at bottom of file */
    
    /* --- CALENDAR CSS (FIX) --- */
    .cal-grid { 
        display: grid; 
        grid-template-columns: repeat(7, 1fr); 
        gap: 5px; 
        margin: 10px 0; 
    }
    .cal-header { 
        text-align: center; 
        padding: 5px; 
        color: #00d4ff; 
        font-family: 'Orbitron'; 
        font-size: 0.8rem; 
        font-weight: bold;
    }
    .cal-day { 
        text-align: center; 
        padding: 5px; 
        min-height: 60px; 
        border-radius: 10px; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        font-size: 0.9rem;
    }
    .cal-day-normal { 
        background: rgba(0, 119, 182, 0.1); 
        border: 1px solid rgba(0, 212, 255, 0.1); 
        color: #caf0f8; 
    }
    .cal-day-today { 
        background: rgba(0, 180, 216, 0.3); 
        border: 2px solid #00d4ff; 
        color: #ffffff; 
        font-weight: bold; 
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    .cal-day-workout { 
        background: rgba(0, 255, 136, 0.1); 
        border: 1px solid #00ff88; 
        color: #00ff88; 
    }
    .cal-icon { font-size: 1rem; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

# Read current page from URL query params
current_page_from_url = get_current_page_from_url()

# --- MOTIVATIONAL QUOTES ---
quotes = [
    ("The only bad workout is the one that didn't happen.", "Unknown"),
    ("Strong is the new beautiful.", "Unknown"),
    ("Your body can stand almost anything. It's your mind you have to convince.", "Unknown"),
    ("Sweat is just fat crying.", "Unknown"),
    ("The pain you feel today will be the strength you feel tomorrow.", "Unknown"),
    ("Fitness is not about being better than someone else. It's about being better than you used to be.", "Unknown"),
    ("She believed she could, so she did.", "R.S. Grey"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("A year from now, you'll wish you had started today.", "Karen Lamb"),
    ("Strong women lift each other up.", "Unknown"),
]

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
    
    # Navigation - using query params for native back gesture support
    st.markdown("## 🧭 Navigation")
    
    nav_options = ["🏠 Home", "📅 Workout Calendar", "💪 Workout Programs", "📚 Exercise Library", "🎬 My Collection"]
    
    # Get current page from URL
    current_page = current_page_from_url
    current_index = nav_options.index(current_page) if current_page in nav_options else 0
    
    # Create a callback function to navigate via query params
    def on_nav_change():
        selected = st.session_state.main_nav
        page_key = PAGE_REVERSE_MAPPING.get(selected, 'home')
        st.query_params['page'] = page_key

    st.radio(
        "Choose a section:",
        nav_options,
        index=current_index,
        label_visibility="collapsed",
        key="main_nav",
        on_change=on_nav_change
    )
    
    # Use URL query params as the source of truth for page
    page = current_page_from_url
    
    st.markdown("---")
    
    # Quick Stats in Sidebar
    df_sidebar = utils.get_workouts()
    total_workouts = len(df_sidebar)
    calendar_data = utils.load_calendar()
    scheduled_days = len(calendar_data)
    
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
    streak_data = utils.get_streak_data()
    st.markdown("### 🔥 Current Streak")
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(255, 165, 0, 0.1)); border-radius: 15px; border: 2px solid rgba(255, 165, 0, 0.4);">
        <div style="font-size: 2rem;">{'🔥' * min(streak_data['current_streak'], 5) if streak_data['current_streak'] > 0 else '💪'}</div>
        <div style="font-family: 'Orbitron', sans-serif; font-size: 2rem; color: #ffa500;">{streak_data['current_streak']}</div>
        <div style="font-family: 'Rajdhani', sans-serif; color: #ffcc80; font-size: 0.8rem;">DAY STREAK</div>
    </div>
    """, unsafe_allow_html=True)

# --- BACK BUTTON (for non-home pages) ---
if page != "🏠 Home":
    # JavaScript-based back button that uses browser history
    st.markdown("""
    <style>
        .back-btn-container {
            margin-bottom: 15px;
        }
        .back-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: rgba(0, 119, 182, 0.2);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 25px;
            color: #00d4ff;
            font-family: 'Rajdhani', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        .back-btn:hover {
            background: rgba(0, 212, 255, 0.3);
            transform: translateX(-5px);
            box-shadow: 0 5px 20px rgba(0, 212, 255, 0.3);
        }
    </style>
    <div class="back-btn-container">
        <a class="back-btn" href="?page=home">
            ⬅️ Retour à l'accueil
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN CONTENT ---

# ===== HOME PAGE =====
if page == "🏠 Home":
    # Header
    st.markdown('<h1 class="main-header">💎 JADE FITNESS HUB 💎</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">YOUR PERSONAL WORKOUT SANCTUARY</p>', unsafe_allow_html=True)
    
    # Welcome Banner with Quote
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
    streak_data = utils.get_streak_data()
    current_streak = streak_data['current_streak']
    best_streak = streak_data['best_streak']
    streak_status = streak_data['streak_status']
    
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
    
    # Streak status message
    if streak_status == 'completed_today':
        status_msg = "✅ Today's workout complete!"
    elif streak_status == 'pending_today':
        status_msg = "⏳ Complete today's workout to keep your streak!"
    elif streak_status == 'at_risk':
        status_msg = "⚠️ Don't break your streak - workout today!"
    else:
        status_msg = "Start a new streak today!"
    
    col_streak1, col_streak2 = st.columns([2, 1])
    
    with col_streak1:
        st.markdown(f"""
        <div class="streak-container">
            <div class="streak-flames">{flame_emoji}</div>
            <div class="streak-number">{current_streak}</div>
            <div class="streak-label">DAY STREAK</div>
            <div class="streak-badge">{streak_badge}</div>
            <p style="color: #ffcc80; font-size: 0.85rem; margin-top: 10px; position: relative; z-index: 1;">{status_msg}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_streak2:
        st.markdown(f"""
        <div style="background: rgba(0, 119, 182, 0.1); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 15px; padding: 15px; text-align: center; height: 100%;">
            <div style="margin-bottom: 15px;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.8rem; color: #00d4ff;">🏆 {best_streak}</div>
                <div style="font-family: 'Rajdhani', sans-serif; color: #90e0ef; font-size: 0.75rem; text-transform: uppercase;">Best Streak</div>
            </div>
            <div>
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.8rem; color: #00ff88;">{streak_data['total_completed']}</div>
                <div style="font-family: 'Rajdhani', sans-serif; color: #90e0ef; font-size: 0.75rem; text-transform: uppercase;">Total Completed</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Today's Workout Section
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_workouts = utils.get_workouts_for_date(today_str)
    
    st.markdown("## 📅 Today's Workout Plan")
    st.markdown(f"*{datetime.now().strftime('%A, %B %d, %Y')}*")
    
    if today_workouts:
        for idx, workout in enumerate(today_workouts):
            completed = workout.get('completed', False)
            status_icon = "✅" if completed else "⏳"
            st.markdown(f"""
            <div class="exercise-row" style="{'opacity: 0.6;' if completed else ''}">
                <span class="exercise-name">{status_icon} {workout.get('name', 'Workout')}</span>
                <span class="exercise-details">{workout.get('type', 'General')} • {workout.get('duration', '30 min')}</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("✓ Complete" if not completed else "↩ Undo", key=f"complete_{idx}"):
                    utils.mark_workout_complete(today_str, idx, not completed)
                    st.rerun()
    else:
        st.info("💡 No workouts scheduled for today. Head to the Calendar to plan your workout!")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("## ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">📅</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Plan</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Plan", key="nav_calendar", use_container_width=True):
            navigate_to("📅 Workout Calendar")
        
    with col2:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">💪</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Progs</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Progs", key="nav_programs", use_container_width=True):
            navigate_to("💪 Workout Programs")
        
    with col3:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎬</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Vids</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Vids", key="nav_collection", use_container_width=True):
            navigate_to("🎬 My Collection")

    with col4:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">📚</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Lib</h4>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Lib", key="nav_library", use_container_width=True):
            navigate_to("📚 Exercise Library")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Weekly Overview
    st.markdown("## 📊 This Week's Progress")
    
    # Get this week's data
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    
    week_cols = st.columns(7)
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    for i, day_col in enumerate(week_cols):
        day_date = start_of_week + timedelta(days=i)
        day_str = day_date.strftime("%Y-%m-%d")
        day_workouts = utils.get_workouts_for_date(day_str)
        is_today = day_date.date() == today.date()
        
        completed_count = sum(1 for w in day_workouts if w.get('completed', False))
        total_count = len(day_workouts)
        
        with day_col:
            bg_color = "rgba(0, 212, 255, 0.2)" if is_today else "rgba(0, 119, 182, 0.1)"
            border_color = "#00d4ff" if is_today else "rgba(0, 212, 255, 0.2)"
            
            status_emoji = "✅" if completed_count == total_count and total_count > 0 else ("🏃" if total_count > 0 else "")
            
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: {bg_color}; border-radius: 15px; border: 1px solid {border_color};">
                <div style="font-family: 'Rajdhani', sans-serif; color: #90e0ef; font-size: 0.8rem;">{days_of_week[i]}</div>
                <div style="font-family: 'Orbitron', sans-serif; color: {'#00d4ff' if is_today else '#caf0f8'}; font-size: 1.3rem; font-weight: bold;">{day_date.day}</div>
                <div style="font-size: 1.2rem; margin-top: 5px;">{status_emoji}</div>
                <div style="color: #48cae4; font-size: 0.7rem;">{f'{completed_count}/{total_count}' if total_count > 0 else '-'}</div>
            </div>
            """, unsafe_allow_html=True)

# ===== CALENDAR PAGE =====
elif page == "📅 Workout Calendar":
    st.markdown('<h1 class="main-header">📅 WORKOUT CALENDAR</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">YOUR ONE-YEAR FITNESS JOURNEY</p>', unsafe_allow_html=True)
    
    # 🔥 STREAK DISPLAY AT TOP OF CALENDAR
    streak_data = utils.get_streak_data()
    current_streak = streak_data['current_streak']
    streak_status = streak_data['streak_status']
    
    # Mini streak display for calendar page
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        flame_emoji = "🔥🔥🔥" if current_streak >= 7 else ("🔥🔥" if current_streak >= 3 else ("🔥" if current_streak >= 1 else "💪"))
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(255, 165, 0, 0.1)); border: 2px solid rgba(255, 165, 0, 0.4); border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px;">
            <span style="font-size: 1.5rem;">{flame_emoji}</span>
            <span style="font-family: 'Orbitron', sans-serif; font-size: 1.8rem; color: #ffa500; margin: 0 10px;">{current_streak}</span>
            <span style="font-family: 'Rajdhani', sans-serif; color: #ffcc80; font-size: 0.9rem; text-transform: uppercase;">Day Streak</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize calendar
    utils.init_calendar()
    
    # One Year Program Info & Reset Button
    calendar_data = utils.load_calendar()
    workout_days = len([d for d in calendar_data if calendar_data[d]])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 180, 216, 0.05)); border: 2px solid rgba(0, 212, 255, 0.3); border-radius: 15px; padding: 15px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="font-family: 'Orbitron', sans-serif; color: #00d4ff; font-size: 1.1rem;">📆 ONE-YEAR PROGRAM</span>
                <span style="color: #90e0ef; font-size: 0.9rem; margin-left: 15px;">{workout_days} workout days planned</span>
            </div>
        </div>
        <div style="color: #48cae4; font-size: 0.8rem; margin-top: 10px;">
            🗓️ Progressive training: Foundation → Beginner → Intermediate → Advanced → Peak Performance
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Reset button with confirmation
    col_reset1, col_reset2, col_reset3 = st.columns([2, 1, 2])
    with col_reset2:
        if st.button("🔄 Generate New Year", use_container_width=True, help="Clear and regenerate a full year of workouts"):
            utils.clear_calendar()
            utils.populate_sample_workouts()
            st.success("🎉 New one-year workout plan generated!")
            st.rerun()
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Convert calendar data to streamlit-calendar events format
    today = datetime.now()
    calendar_events = []
    
    # Color mapping for workout types
    workout_colors = {
        "Lower Body": "#ff6b6b",
        "Upper Body": "#4ecdc4",
        "HIIT": "#ff9f43",
        "Cardio": "#ee5a24",
        "Full Body": "#00d4ff",
        "Yoga": "#a29bfe",
        "Pilates": "#fd79a8",
        "Stretching": "#55efc4",
        "Core": "#ffeaa7",
        "Strength": "#74b9ff",
        "Dance": "#e056fd",
    }
    
    for date_str, workouts in calendar_data.items():
        for idx, workout in enumerate(workouts):
            workout_type = workout.get('type', 'Workout')
            is_completed = workout.get('completed', False)
            
            # Choose color based on type and completion
            base_color = workout_colors.get(workout_type, "#00d4ff")
            if is_completed:
                color = "#00ff88"  # Green for completed
            else:
                color = base_color
            
            event = {
                "title": f"{'✅' if is_completed else '💪'} {workout.get('name', 'Workout')}",
                "start": date_str,
                "end": date_str,
                "backgroundColor": color,
                "borderColor": color,
                "textColor": "#ffffff" if not is_completed else "#000000",
                "extendedProps": {
                    "type": workout_type,
                    "duration": workout.get('duration', ''),
                    "notes": workout.get('notes', ''),
                    "completed": is_completed,
                    "index": idx
                }
            }
            calendar_events.append(event)
    
    # Streamlit Calendar Options - Dark futuristic theme
    calendar_options = {
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,listMonth"
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "22:00:00",
        "initialDate": today.strftime("%Y-%m-%d"),
        "editable": False,
        "selectable": True,
        "selectMirror": True,
        "dayMaxEvents": 3,
        "weekends": True,
        "nowIndicator": True,
        "height": 650,
        "eventDisplay": "block",
        "displayEventTime": False,
    }
    
    # Custom CSS for the calendar to match our dark theme
    custom_css = """
        .fc {
            font-family: 'Rajdhani', sans-serif;
        }
        .fc-theme-standard td, .fc-theme-standard th {
            border-color: rgba(0, 212, 255, 0.2);
        }
        .fc-theme-standard .fc-scrollgrid {
            border-color: rgba(0, 212, 255, 0.3);
        }
        .fc .fc-daygrid-day-number {
            color: #90e0ef;
            font-weight: 600;
        }
        .fc .fc-col-header-cell-cushion {
            color: #00d4ff;
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
        }
        .fc-day-today {
            background: rgba(0, 212, 255, 0.15) !important;
        }
        .fc-day-today .fc-daygrid-day-number {
            color: #00d4ff !important;
            font-weight: 700;
        }
        .fc .fc-button-primary {
            background: linear-gradient(135deg, #0077b6, #00b4d8);
            border-color: rgba(0, 212, 255, 0.5);
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
        }
        .fc .fc-button-primary:hover {
            background: linear-gradient(135deg, #00b4d8, #00d4ff);
        }
        .fc .fc-button-primary:not(:disabled).fc-button-active {
            background: linear-gradient(135deg, #00d4ff, #48cae4);
        }
        .fc-toolbar-title {
            color: #00d4ff !important;
            font-family: 'Orbitron', sans-serif !important;
        }
        .fc-event {
            border-radius: 6px;
            font-size: 0.75rem;
            padding: 2px 4px;
            font-weight: 600;
        }
        .fc-daygrid-event {
            margin: 1px 2px;
        }
        .fc-h-event {
            border: none;
        }
        .fc .fc-list-event:hover td {
            background: rgba(0, 212, 255, 0.1);
        }
        .fc-list-day-cushion {
            background: rgba(0, 30, 60, 0.8) !important;
        }
        .fc-list-day-text, .fc-list-day-side-text {
            color: #00d4ff !important;
        }
        .fc-popover {
            background: rgba(10, 15, 30, 0.95);
            border-color: rgba(0, 212, 255, 0.3);
        }
        .fc-popover-header {
            background: rgba(0, 119, 182, 0.3);
            color: #00d4ff;
        }
        .fc-more-link {
            color: #00d4ff !important;
        }
    """
    
    # Render the calendar
    calendar_result = st_calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css=custom_css,
        key="fitness_calendar"
    )
    
    # Handle calendar interactions
    if calendar_result:
        if "dateClick" in calendar_result:
            clicked_date = calendar_result["dateClick"]["date"]
            st.session_state.selected_calendar_date = clicked_date
        
        if "eventClick" in calendar_result:
            event_data = calendar_result["eventClick"]["event"]
            st.info(f"📋 **{event_data.get('title', 'Workout')}**\n\n"
                   f"Type: {event_data.get('extendedProps', {}).get('type', 'N/A')}\n\n"
                   f"Duration: {event_data.get('extendedProps', {}).get('duration', 'N/A')}\n\n"
                   f"Notes: {event_data.get('extendedProps', {}).get('notes', 'No notes')}")
    
    # Legend
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin: 20px 0; padding: 15px; background: rgba(0, 30, 60, 0.4); border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.2);">
        <span style="color: #00ff88; font-size: 0.85rem; padding: 5px 10px; background: rgba(0, 255, 136, 0.1); border-radius: 20px;">✅ Completed</span>
        <span style="color: #ff6b6b; font-size: 0.85rem; padding: 5px 10px; background: rgba(255, 107, 107, 0.1); border-radius: 20px;">🦵 Lower Body</span>
        <span style="color: #4ecdc4; font-size: 0.85rem; padding: 5px 10px; background: rgba(78, 205, 196, 0.1); border-radius: 20px;">💪 Upper Body</span>
        <span style="color: #ff9f43; font-size: 0.85rem; padding: 5px 10px; background: rgba(255, 159, 67, 0.1); border-radius: 20px;">⚡ HIIT</span>
        <span style="color: #a29bfe; font-size: 0.85rem; padding: 5px 10px; background: rgba(162, 155, 254, 0.1); border-radius: 20px;">🧘 Yoga</span>
        <span style="color: #00d4ff; font-size: 0.85rem; padding: 5px 10px; background: rgba(0, 212, 255, 0.1); border-radius: 20px;">🏋️ Full Body</span>
    </div>
    """, unsafe_allow_html=True)
    
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
            utils.add_workout_to_calendar(date_str, workout_data)
            st.success(f"🎉 Workout added for {selected_date.strftime('%B %d, %Y')}!")
            st.balloons()
            st.rerun()
        else:
            st.warning("⚠️ Please enter a workout name!")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # View/Edit Workouts for Selected Date
    st.markdown("## 📋 Workouts for Selected Date")
    view_date = st.date_input("View workouts for:", selected_date, key="view_date")
    view_date_str = view_date.strftime("%Y-%m-%d")
    date_workouts = utils.get_workouts_for_date(view_date_str)
    
    if date_workouts:
        # Check if any workouts are incomplete
        has_incomplete = any(not w.get('completed', False) for w in date_workouts)
        all_complete = all(w.get('completed', False) for w in date_workouts)
        
        # Show "Confirm All Complete" button if there are incomplete workouts
        if has_incomplete:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 200, 100, 0.05)); border: 2px solid rgba(0, 255, 136, 0.3); border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px;">
                <p style="color: #90e0ef; margin-bottom: 10px;">Complete all workouts to maintain your streak! 🔥</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ Mark All as Complete", key=f"complete_all_{view_date_str}", use_container_width=True, type="primary"):
                utils.confirm_workout_completed(view_date_str)
                st.success("🎉 All workouts marked complete! Your streak continues!")
                st.balloons()
                st.rerun()
        elif all_complete:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 200, 100, 0.1)); border: 2px solid rgba(0, 255, 136, 0.4); border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px;">
                <span style="font-size: 1.5rem;">🏆</span>
                <span style="font-family: 'Rajdhani', sans-serif; color: #00ff88; font-size: 1.1rem; margin-left: 10px;">All workouts complete for this day!</span>
            </div>
            """, unsafe_allow_html=True)
        
        for idx, workout in enumerate(date_workouts):
            with st.expander(f"{'✅' if workout.get('completed') else '⏳'} {workout.get('name', 'Workout')} - {workout.get('type', '')}"):
                st.write(f"**Duration:** {workout.get('duration', 'Not specified')}")
                st.write(f"**Notes:** {workout.get('notes', 'No notes')}")
                st.write(f"**Status:** {'Completed ✅' if workout.get('completed') else 'Pending ⏳'}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✅ Toggle Complete", key=f"toggle_{view_date_str}_{idx}"):
                        utils.mark_workout_complete(view_date_str, idx, not workout.get('completed', False))
                        st.rerun()
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{view_date_str}_{idx}"):
                        utils.remove_workout_from_calendar(view_date_str, idx)
                        st.success("Workout removed!")
                        st.rerun()
    else:
        st.info(f"💡 No workouts scheduled for {view_date.strftime('%B %d, %Y')}")

# ===== WORKOUT PROGRAMS PAGE =====
elif page == "💪 Workout Programs":
    st.markdown('<h1 class="main-header">💪 WORKOUT PROGRAMS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">CURATED PROGRAMS FOR WOMEN</p>', unsafe_allow_html=True)
    
    programs = utils.get_workout_programs()
    
    # Program Selection
    if 'selected_program' not in st.session_state:
        st.session_state.selected_program = None
    
    # Show program list if no program selected
    if st.session_state.selected_program is None:
        st.markdown("## 🎯 Choose Your Program")
        
        # Display program cards in a cleaner layout
        for program_id, program in programs.items():
            with st.container():
                st.markdown(f"""
                <div class="program-card" style="margin-bottom: 15px;">
                    <div class="program-title">{program['name']}</div>
                    <p style="color: #caf0f8; font-family: 'Rajdhani', sans-serif; margin: 10px 0;">{program['description']}</p>
                    <div class="program-meta">
                        <span class="program-tag">📅 {program['duration']}</span>
                        <span class="program-tag">📊 {program['level']}</span>
                        <span class="program-tag">🎯 {program['goal']}</span>
                        <span class="program-tag">🗓️ {program['days_per_week']} days/week</span>
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
        
        # Back button at top - more prominent
        col_back, col_title = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ Back", key="back_programs", use_container_width=True, type="secondary"):
                st.session_state.selected_program = None
                st.rerun()
        with col_title:
            st.markdown(f"## 📋 {selected['name']}")
        
        st.markdown(f"*{selected['description']}*")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ===== VISUAL PROGRAM OVERVIEW =====
        col1, col2 = st.columns(2)
        
        with col1:
            # Program Stats Grid
            st.markdown(f"""
            <div class="stats-grid">
                <div class="mini-stat">
                    <div class="mini-stat-icon">📅</div>
                    <div class="mini-stat-value">{selected['duration'].split()[0]}</div>
                    <div class="mini-stat-label">Weeks</div>
                </div>
                <div class="mini-stat">
                    <div class="mini-stat-icon">🗓️</div>
                    <div class="mini-stat-value">{selected['days_per_week']}</div>
                    <div class="mini-stat-label">Days/Week</div>
                </div>
                <div class="mini-stat">
                    <div class="mini-stat-icon">📊</div>
                    <div class="mini-stat-value">{selected['level'][:3]}</div>
                    <div class="mini-stat-label">Level</div>
                </div>
                <div class="mini-stat">
                    <div class="mini-stat-icon">🔥</div>
                    <div class="mini-stat-value">30</div>
                    <div class="mini-stat-label">Min/Day</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Weekly Schedule Visual
            days_active = selected['days_per_week']
            day_labels = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
            active_days = [i < days_active for i in range(7)]
            
            days_html = ""
            for i, (label, active) in enumerate(zip(day_labels, active_days)):
                class_name = "active" if active else "rest"
                days_html += f'<div class="day-circle {class_name}">{label}</div>'
            
            st.markdown(f"""
            <div style="padding: 15px;">
                <p style="color: #90e0ef; font-family: 'Rajdhani', sans-serif; margin-bottom: 10px; font-size: 0.9rem;">📅 WEEKLY SCHEDULE</p>
                <div class="week-visual">
                    {days_html}
                </div>
                <p style="color: #48cae4; font-size: 0.8rem; text-align: center;">
                    <span style="color: #00d4ff;">●</span> Workout Days &nbsp;&nbsp;
                    <span style="color: #48cae4;">●</span> Rest Days
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ===== MUSCLE GROUP TARGETING =====
        st.markdown("### 💪 Muscle Groups Targeted")
        
        # Program-specific muscle focus
        muscle_targets = {
            'beginner_full_body': {'Legs': 80, 'Core': 70, 'Arms': 60, 'Back': 65, 'Chest': 55, 'Glutes': 75},
            'slim_thick': {'Glutes': 95, 'Legs': 90, 'Core': 70, 'Back': 50, 'Arms': 40, 'Chest': 30},
            'yoga_flexibility': {'Core': 85, 'Back': 80, 'Legs': 75, 'Arms': 60, 'Chest': 50, 'Glutes': 65},
            'hiit_fat_burn': {'Legs': 85, 'Core': 80, 'Arms': 70, 'Glutes': 75, 'Back': 65, 'Chest': 60},
            'booty_builder': {'Glutes': 100, 'Legs': 90, 'Core': 65, 'Back': 55, 'Arms': 35, 'Chest': 25}
        }
        
        muscles = muscle_targets.get(st.session_state.selected_program, {'Full Body': 80})
        
        # Display muscle chart using Streamlit progress bars
        for muscle, percent in sorted(muscles.items(), key=lambda x: x[1], reverse=True):
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.markdown(f"<span style='color: #90e0ef; font-family: Rajdhani, sans-serif; font-size: 0.95rem;'>{muscle}</span>", unsafe_allow_html=True)
            with col2:
                st.progress(percent / 100)
            with col3:
                st.markdown(f"<span style='color: #00d4ff; font-family: Orbitron, sans-serif; font-size: 0.9rem;'>{percent}%</span>", unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ===== INTENSITY LEVEL =====
        st.markdown("### ⚡ Workout Intensity")
        
        intensity_levels = {
            'beginner_full_body': 3,
            'slim_thick': 4,
            'yoga_flexibility': 2,
            'hiit_fat_burn': 5,
            'booty_builder': 4
        }
        
        intensity = intensity_levels.get(st.session_state.selected_program, 3)
        intensity_labels = {1: 'Light', 2: 'Easy', 3: 'Moderate', 4: 'Intense', 5: 'Extreme'}
        intensity_colors = {1: '🟢', 2: '🟢', 3: '🟡', 4: '🟠', 5: '🔴'}
        
        # Display intensity using columns with emojis
        int_col1, int_col2 = st.columns([2, 3])
        with int_col1:
            intensity_display = ""
            for i in range(5):
                if i < intensity:
                    intensity_display += "🔥"
                else:
                    intensity_display += "⬜"
            st.markdown(f"<div style='font-size: 1.8rem; letter-spacing: 5px;'>{intensity_display}</div>", unsafe_allow_html=True)
        with int_col2:
            st.markdown(f"""
            <div style="padding: 15px; background: rgba(0, 119, 182, 0.1); border-radius: 15px; border-left: 4px solid #00d4ff;">
                <span style="font-family: 'Orbitron', sans-serif; color: #00d4ff; font-size: 1.3rem;">
                    {intensity_colors[intensity]} {intensity_labels[intensity]}
                </span>
                <p style="color: #90e0ef; font-size: 0.85rem; margin-top: 5px;">
                    {['', 'Perfect for recovery days', 'Great for beginners', 'Balanced workout', 'Push your limits!', 'Maximum effort required!'][intensity]}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ===== DETAILED SCHEDULE =====
        st.markdown("### 📋 Detailed Schedule")
        
        # Check if program has 'phases' (one-year program) or 'schedule' (regular programs)
        if 'phases' in selected:
            # One-year transformation program structure
            for phase_name, phase_data in selected['phases'].items():
                st.markdown(f"## 🚀 {phase_name}")
                st.markdown(f"**Focus:** {phase_data['focus']}")
                st.markdown(f"**Intensity:** {phase_data['intensity']}")
                st.markdown("---")
                
                for week_range, week_schedule in phase_data['weeks'].items():
                    with st.expander(f"📅 {week_range}", expanded=False):
                        for day_name, exercises in week_schedule.items():
                            st.markdown(f"**{day_name}**")
                            for exercise in exercises:
                                if exercise['sets'] == 0:
                                    # Sub-item (like circuit details)
                                    st.markdown(f"<span style='color: #90e0ef; margin-left: 20px;'>{exercise['name']}</span>", unsafe_allow_html=True)
                                else:
                                    rest_info = f" | Rest: {exercise['rest']}" if exercise['rest'] else ""
                                    st.markdown(f"""
                                    <div class="exercise-row">
                                        <span class="exercise-name">{exercise['name']}</span>
                                        <span class="exercise-details">{exercise['sets']} sets × {exercise['reps']}{rest_info}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                            st.markdown("---")
            
            # Show milestone rewards for one-year program
            if 'milestone_rewards' in selected:
                st.markdown("### 🏆 Milestone Rewards")
                for milestone, reward in selected['milestone_rewards'].items():
                    st.markdown(f"**{milestone}:** {reward}")
        
        elif 'schedule' in selected:
            # Regular program structure
            for week_name, week_schedule in selected['schedule'].items():
                st.markdown(f"### 📅 {week_name}")
                
                for day_name, day_data in week_schedule.items():
                    with st.expander(f"**{day_name}** - {day_data['focus']}", expanded=False):
                        st.markdown(f"**🎯 Focus:** {day_data['focus']}")
                        st.markdown("---")
                        
                        for exercise in day_data['exercises']:
                            rest_info = f" | Rest: {exercise['rest']}" if exercise['rest'] else ""
                            st.markdown(f"""
                            <div class="exercise-row">
                                <span class="exercise-name">{exercise['name']}</span>
                                <span class="exercise-details">{exercise['sets']} sets × {exercise['reps']}{rest_info}</span>
                            </div>
                            """, unsafe_allow_html=True)
        
        # Recommended Videos Section
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 🎬 Recommended Workout Videos")
        st.markdown("*Watch these videos to learn proper form and technique!*")
        
        # Program-specific video recommendations
        program_videos = {
            'beginner_full_body': [
                ('Full Body Beginner Workout', 'https://www.youtube.com/watch?v=UItWltVZZmE'),
                ('20 Min Full Body Stretch', 'https://www.youtube.com/watch?v=g_tea8ZNk5A'),
            ],
            'slim_thick': [
                ('Booty Workout - Grow Glutes', 'https://www.youtube.com/watch?v=ZYxAHoOweGk'),
                ('15 Min Leg Workout', 'https://www.youtube.com/watch?v=XF5clnw4QOM'),
            ],
            'yoga_flexibility': [
                ('30 Min Yoga Flow', 'https://www.youtube.com/watch?v=oBu-pQG6sTY'),
                ('Morning Yoga Stretch', 'https://www.youtube.com/watch?v=4pKly2JojMw'),
            ],
            'hiit_fat_burn': [
                ('15 Min Fat Burning HIIT', 'https://www.youtube.com/watch?v=ml6cT4AZdqI'),
                ('Dance Party Workout', 'https://www.youtube.com/watch?v=YO0E9J-LlEE'),
            ],
            'booty_builder': [
                ('25 Min Booty Workout', 'https://www.youtube.com/watch?v=ZYxAHoOweGk'),
                ('30 Min Walking Workout', 'https://www.youtube.com/watch?v=5WzKKrFwUGQ'),
            ]
        }
        
        videos = program_videos.get(st.session_state.selected_program, [])
        
        if videos:
            cols = st.columns(len(videos))
            for idx, (title, url) in enumerate(videos):
                with cols[idx]:
                    if st.button(f"▶️ {title}", key=f"rec_vid_{idx}", use_container_width=True):
                        st.video(url)
        else:
            st.info("📺 Video recommendations coming soon!")

# ===== EXERCISE LIBRARY PAGE =====
elif page == "📚 Exercise Library":
    st.markdown('<h1 class="main-header">📚 EXERCISE LIBRARY</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">LEARN PROPER FORM WITH GIF DEMONSTRATIONS</p>', unsafe_allow_html=True)
    
    # Search and Filter Section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search exercises", placeholder="Search by name or muscle group...")
    with col2:
        category_filter = st.selectbox("📂 Category", EXERCISE_CATEGORIES)
    with col3:
        difficulty_filter = st.selectbox("📊 Difficulty", DIFFICULTY_LEVELS)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Get filtered exercises
    if search_query:
        exercises = search_exercises(search_query)
    else:
        exercises = EXERCISE_LIBRARY.copy()
    
    # Apply category filter
    if category_filter != "All":
        exercises = {k: v for k, v in exercises.items() if v["category"] == category_filter}
    
    # Apply difficulty filter
    if difficulty_filter != "All":
        exercises = {k: v for k, v in exercises.items() if v["difficulty"] == difficulty_filter}
    
    # Display exercise count
    st.markdown(f"### 💪 {len(exercises)} Exercises Found")
    
    # Initialize selected exercise in session state
    if 'selected_exercise' not in st.session_state:
        st.session_state.selected_exercise = None
    
    # Display exercise list or selected exercise
    if st.session_state.selected_exercise is None:
        # Display exercise cards in grid
        exercise_list = list(exercises.items())
        
        for i in range(0, len(exercise_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(exercise_list):
                    key, exercise = exercise_list[i + j]
                    with cols[j]:
                        # Exercise card
                        st.markdown(f"""
                        <div class="program-card" style="text-align: center; min-height: 320px;">
                            <div style="font-size: 2rem; margin-bottom: 10px;">
                                {'🦵' if exercise['category'] == 'Lower Body' else '💪' if exercise['category'] == 'Upper Body' else '🎯' if exercise['category'] == 'Core' else '❤️' if exercise['category'] == 'Cardio' else '🧘'}
                            </div>
                            <div class="program-title" style="font-size: 1.1rem;">{exercise['name']}</div>
                            <div class="program-meta" style="justify-content: center; margin: 10px 0;">
                                <span class="program-tag">{exercise['category']}</span>
                                <span class="program-tag">{exercise['difficulty']}</span>
                            </div>
                            <p style="color: #90e0ef; font-size: 0.85rem; margin: 10px 0;">
                                {', '.join(exercise['muscle_groups'][:3])}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"📖 View Exercise", key=f"view_ex_{key}", use_container_width=True):
                            st.session_state.selected_exercise = key
                            st.rerun()
    
    else:
        # Display selected exercise details
        exercise = EXERCISE_LIBRARY[st.session_state.selected_exercise]
        
        # Back button - more prominent
        col_back, col_title = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ Back", key="back_exercises", use_container_width=True, type="secondary"):
                st.session_state.selected_exercise = None
                st.rerun()
        with col_title:
            st.markdown(f"## {exercise['name']}")
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Exercise header
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="program-meta">
                <span class="program-tag">{exercise['category']}</span>
                <span class="program-tag">{exercise['difficulty']}</span>
                <span class="program-tag">{exercise['equipment']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Muscle Groups:** {', '.join(exercise['muscle_groups'])}")
            st.markdown(f"**Recommended:** {exercise['sets_range']} sets × {exercise['reps_range']}")
        
        with col2:
            # Display GIF
            st.markdown("### 🎬 Demo")
            try:
                st.image(exercise['gif_url'], use_container_width=True)
            except:
                st.info("GIF loading... Click the video button below for a demonstration.")
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Instructions tabs - now with 3D View
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Instructions", "🎮 3D View", "⚠️ Common Mistakes", "💡 Tips", "🎬 Video"])
        
        with tab1:
            st.markdown("### Setup")
            st.markdown(f"*{exercise['instructions']['setup']}*")
            
            st.markdown("### Step-by-Step Execution")
            for i, step in enumerate(exercise['instructions']['execution'], 1):
                st.markdown(f"""
                <div class="exercise-row">
                    <span class="exercise-name">Step {i}</span>
                    <span class="exercise-details">{step}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### Breathing")
            st.info(f"🫁 {exercise['instructions']['breathing']}")
        
        with tab2:
            st.markdown("### 🎬 Exercise Demonstration")
            st.markdown("*Watch the animated GIF to learn proper form!*")
            
            # Render the exercise GIF demo
            render_exercise_demo(
                exercise_name=exercise['name'],
                exercise_type=exercise.get('category', 'general')
            )
            
            st.markdown("""
            <div style="background: rgba(0, 119, 182, 0.1); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 10px; padding: 15px; margin-top: 15px;">
                <h4 style="color: #00d4ff; margin-top: 0;">💡 Tips</h4>
                <ul style="color: #90e0ef; margin-bottom: 0;">
                    <li><strong>Focus:</strong> Watch the movement pattern carefully</li>
                    <li><strong>Form:</strong> Match your body position to the demo</li>
                    <li><strong>Pace:</strong> Start slow, then match the rhythm</li>
                    <li><strong>Mirror:</strong> Practice in front of a mirror</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### Common Mistakes & Fixes")
            for mistake in exercise['instructions']['common_mistakes']:
                parts = mistake.split(" - ")
                if len(parts) == 2:
                    st.markdown(f"""
                    <div style="background: rgba(255, 107, 107, 0.1); border-left: 3px solid #ff6b6b; padding: 10px 15px; margin: 10px 0; border-radius: 0 10px 10px 0;">
                        <strong style="color: #ff6b6b;">❌ {parts[0]}</strong><br>
                        <span style="color: #90e0ef;">✅ Fix: {parts[1]}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(f"⚠️ {mistake}")
        
        with tab4:
            st.markdown("### Pro Tips")
            st.success(f"💡 {exercise['instructions']['tips']}")
            
            # Muscle target visualization
            st.markdown("### Muscles Targeted")
            for muscle in exercise['muscle_groups']:
                st.progress(0.8, text=f"💪 {muscle}")
        
        with tab5:
            st.markdown("### Video Demonstration")
            if exercise.get('video_url'):
                if st.button("▶️ Watch Tutorial Video", use_container_width=True):
                    st.video(exercise['video_url'])
            else:
                st.info("Video coming soon!")
    
# ===== MY COLLECTION PAGE =====
elif page == "🎬 My Collection":
    st.markdown('<h1 class="main-header">🎬 MY COLLECTION</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">YOUR SAVED WORKOUT VIDEOS</p>', unsafe_allow_html=True)
    
    # Add Workout Section
    st.markdown("## ➕ Add New Video")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        url_input = st.text_input("🔗 YouTube URL", placeholder="Paste video link here...")
    with col2:
        category_input = st.selectbox(
            "📂 Category", 
            ["💪 Strength", "❤️ Cardio", "🧘 Yoga", "🩰 Pilates", "💃 Dance", "🏃 HIIT", "🧘‍♀️ Stretching"]
        )
    
    clean_category = category_input.split(" ", 1)[1] if " " in category_input else category_input
    
    if st.button("✨ Add to Collection", use_container_width=True):
        if url_input:
            with st.spinner("🔮 Fetching video magic..."):
                success = utils.add_workout(url_input, clean_category)
                if success:
                    st.success("🎉 Workout added successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Couldn't find the video. Please check the URL.")
        else:
            st.warning("⚠️ Please paste a YouTube URL first!")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Load Data
    df = utils.get_workouts()
    
    # Stats Section
    if not df.empty:
        total = len(df)
        categories = df['category'].value_counts()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Total Videos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            strength_count = categories.get('Strength', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{strength_count}</div>
                <div class="stat-label">💪 Strength</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            cardio_count = categories.get('Cardio', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{cardio_count}</div>
                <div class="stat-label">❤️ Cardio</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            yoga_count = categories.get('Yoga', 0) + categories.get('Pilates', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{yoga_count}</div>
                <div class="stat-label">🧘 Mind & Body</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Section Title
    st.markdown("## 🎬 Your Workout Videos")
    
    # Category Filter
    if not df.empty:
        all_categories = ["All"] + list(df['category'].unique())
        selected_category = st.selectbox("🔍 Filter by Category", all_categories, key="filter")
        
        if selected_category != "All":
            df = df[df['category'] == selected_category]
    
    # If empty, show instructions and starter videos option
    if df.empty:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(0, 180, 216, 0.05), rgba(0, 119, 182, 0.1)); border-radius: 20px; border: 1px dashed rgba(0, 212, 255, 0.3);">
            <div style="font-size: 4rem; margin-bottom: 20px;">🏋️‍♀️</div>
            <h3 style="color: #caf0f8; font-family: 'Orbitron', sans-serif;">No Workouts Yet!</h3>
            <p style="color: #90e0ef; font-family: 'Rajdhani', sans-serif; font-size: 1.1rem;">
                Start building your collection by adding your favorite workout videos above!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Option to load starter videos
        st.markdown("### ✨ Or Get Started with Our Curated Collection!")
        st.markdown("*We've handpicked 12 amazing workout videos from top fitness creators to help you start your journey!*")
        
        if st.button("🚀 Load Starter Workout Collection", use_container_width=True):
            with st.spinner("✨ Loading your starter collection..."):
                utils.seed_starter_videos()
                st.success("🎉 12 curated workout videos have been added to your collection!")
                st.balloons()
                st.rerun()
        
        # Show preview of starter videos
        st.markdown("### 🎬 Preview of Starter Collection")
        starter_videos = utils.get_starter_videos()
        
        cols = st.columns(4)
        for idx, video in enumerate(starter_videos[:4]):
            with cols[idx]:
                st.markdown(f"""
                <div class="workout-card" style="padding: 10px;">
                    <img src="{video['thumbnail']}" style="width: 100%; border-radius: 10px; opacity: 0.8;">
                    <p style="color: #90e0ef; font-size: 0.8rem; margin-top: 8px; text-align: center;">{video['title'][:30]}...</p>
                </div>
                """, unsafe_allow_html=True)
    
    # DISPLAY AS GRID (3 Cards per row)
    else:
        df = df.iloc[::-1].reset_index(drop=True)
        
        for i in range(0, len(df), 3):
            cols = st.columns(3, gap="medium")
            for j in range(3):
                if i + j < len(df):
                    row = df.iloc[i + j]
                    with cols[j]:
                        st.markdown('<div class="workout-card">', unsafe_allow_html=True)
                        st.image(row['thumbnail'], use_container_width=True)
                        
                        title = row['title']
                        if len(title) > 50:
                            title = title[:47] + "..."
                        st.markdown(f"### {title}")
                        
                        category_emojis = {
                            'Strength': '💪', 'Cardio': '❤️', 'Yoga': '🧘',
                            'Pilates': '🩰', 'Dance': '💃', 'HIIT': '🏃', 'Stretching': '🧘‍♀️'
                        }
                        emoji = category_emojis.get(row['category'], '🎯')
                        
                        st.markdown(f"""
                        <span class="category-badge">{emoji} {row['category']}</span>
                        <p class="channel-name">📺 {row['channel']}</p>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"▶️ Watch Now", key=f"btn_{i+j}", use_container_width=True):
                            st.video(row['url'])
                        
                        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 20px; opacity: 0.7;">
    <p style="font-family: 'Rajdhani', sans-serif; color: #48cae4; font-size: 0.9rem;">
        Made with 💙 for Jade | Stay Strong, Stay Beautiful ✨
    </p>
</div>
""", unsafe_allow_html=True)

# --- CYBERPUNK FLOATING NAVIGATION BAR ---
st.markdown("""
<style>
    /* ===== CYBERPUNK GLASSMORPHISM NAV BAR ===== */
    
    /* The floating glass pill container - targets the LAST horizontal block (nav buttons) */
    [data-testid="stBottom"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: transparent !important;
        padding: 0 !important;
        z-index: 999999 !important;
    }
    
    [data-testid="stBottom"] > div {
        background: transparent !important;
        padding: 15px !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    [data-testid="stBottom"] [data-testid="stHorizontalBlock"] {
        background: rgba(10, 15, 30, 0.85) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 35px !important;
        padding: 8px 15px !important;
        max-width: 400px !important;
        width: 90% !important;
        margin: 0 auto !important;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.5),
            0 0 30px rgba(0, 212, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
        gap: 5px !important;
    }
    
    /* Column styling */
    [data-testid="stBottom"] [data-testid="column"] {
        padding: 0 !important;
        flex: 1 !important;
    }
    
    /* FORCE transparent buttons - override global theme */
    [data-testid="stBottom"] .stButton > button,
    [data-testid="stBottom"] .stButton button,
    [data-testid="stBottom"] button {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 12px 8px !important;
        font-size: 1.5rem !important;
        color: #90e0ef !important;
        border-radius: 18px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        min-height: 50px !important;
        line-height: 1 !important;
        -webkit-tap-highlight-color: transparent !important;
        filter: drop-shadow(0 0 6px rgba(0, 212, 255, 0.4)) !important;
    }
    
    [data-testid="stBottom"] .stButton > button:hover,
    [data-testid="stBottom"] .stButton button:hover,
    [data-testid="stBottom"] button:hover {
        background: rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
        transform: scale(1.15) translateY(-3px) !important;
        box-shadow: none !important;
        filter: drop-shadow(0 0 15px rgba(0, 212, 255, 0.8)) !important;
    }
    
    [data-testid="stBottom"] .stButton > button:active,
    [data-testid="stBottom"] button:active {
        transform: scale(0.95) !important;
    }
    
    /* Add bottom padding to content */
    .main .block-container {
        padding-bottom: 100px !important;
    }
    
    /* Hide sidebar on mobile */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Bottom navigation using Streamlit's bottom container
with st.container():
    bot_col1, bot_col2, bot_col3, bot_col4, bot_col5 = st.columns(5)
    
    with bot_col1:
        if st.button("🏠", key="mob_home", use_container_width=True):
            navigate_to("🏠 Home")
    
    with bot_col2:
        if st.button("📅", key="mob_cal", use_container_width=True):
            navigate_to("📅 Workout Calendar")
    
    with bot_col3:
        if st.button("💪", key="mob_prog", use_container_width=True):
            navigate_to("💪 Workout Programs")
    
    with bot_col4:
        if st.button("📚", key="mob_lib", use_container_width=True):
            navigate_to("📚 Exercise Library")
    
    with bot_col5:
        if st.button("🎬", key="mob_col", use_container_width=True):
            navigate_to("🎬 My Collection")