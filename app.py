import streamlit as st
import utils
import pandas as pd
from datetime import datetime, timedelta
import calendar
import random

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Jade Fitness Hub", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

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
</style>
""", unsafe_allow_html=True)

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
    
    # Navigation
    st.markdown("## 🧭 Navigation")
    page = st.radio(
        "Choose a section:",
        ["🏠 Home", "📅 Workout Calendar", "💪 Workout Programs", "🎬 My Collection"],
        label_visibility="collapsed"
    )
    
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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">📅</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Plan Workout</h4>
            <p style="color: #90e0ef; font-size: 0.9rem;">Schedule your workouts in the calendar</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">💪</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Browse Programs</h4>
            <p style="color: #90e0ef; font-size: 0.9rem;">Explore curated workout programs</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="action-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎬</div>
            <h4 style="color: #00d4ff; margin: 10px 0;">Watch Videos</h4>
            <p style="color: #90e0ef; font-size: 0.9rem;">Access your saved workout videos</p>
        </div>
        """, unsafe_allow_html=True)
    
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
    st.markdown('<p class="sub-header">PLAN YOUR FITNESS JOURNEY</p>', unsafe_allow_html=True)
    
    # Initialize calendar
    utils.init_calendar()
    
    # Calendar Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    if 'calendar_month' not in st.session_state:
        st.session_state.calendar_month = datetime.now().month
    if 'calendar_year' not in st.session_state:
        st.session_state.calendar_year = datetime.now().year
    
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
    
    # Day headers
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    header_cols = st.columns(7)
    for i, day in enumerate(days):
        with header_cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; color: #00d4ff; font-family: 'Orbitron', sans-serif; font-weight: 600;">
                {day}
            </div>
            """, unsafe_allow_html=True)
    
    # Calendar days
    today = datetime.now()
    calendar_data = utils.load_calendar()
    
    for week in month_days:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown("<div style='min-height: 100px;'></div>", unsafe_allow_html=True)
                else:
                    date_str = f"{st.session_state.calendar_year}-{st.session_state.calendar_month:02d}-{day:02d}"
                    is_today = (day == today.day and 
                               st.session_state.calendar_month == today.month and 
                               st.session_state.calendar_year == today.year)
                    has_workouts = date_str in calendar_data and len(calendar_data[date_str]) > 0
                    workout_count = len(calendar_data.get(date_str, []))
                    
                    border_color = "#00d4ff" if is_today else ("rgba(0, 212, 255, 0.5)" if has_workouts else "rgba(0, 212, 255, 0.2)")
                    bg_color = "rgba(0, 180, 216, 0.2)" if is_today else ("rgba(0, 212, 255, 0.1)" if has_workouts else "rgba(0, 119, 182, 0.1)")
                    
                    workout_dots = "".join([f"<span class='calendar-workout-indicator'></span>" for _ in range(min(workout_count, 3))])
                    
                    st.markdown(f"""
                    <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 10px; padding: 10px; min-height: 80px; text-align: center; transition: all 0.3s ease;">
                        <div style="font-family: 'Orbitron', sans-serif; color: {'#00d4ff' if is_today else '#caf0f8'}; font-size: 1.2rem; font-weight: {'700' if is_today else '400'};">{day}</div>
                        <div style="margin-top: 5px;">{workout_dots}</div>
                        <div style="color: #90e0ef; font-size: 0.7rem; margin-top: 5px;">{f'{workout_count} workout{"s" if workout_count != 1 else ""}' if has_workouts else ''}</div>
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
        
        # Back button at top
        if st.button("⬅️ Back to All Programs", use_container_width=False):
            st.session_state.selected_program = None
            st.rerun()
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        st.markdown(f"## 📋 {selected['name']}")
        st.markdown(f"*{selected['description']}*")
        
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
        
        muscle_bars_html = ""
        for muscle, percent in sorted(muscles.items(), key=lambda x: x[1], reverse=True):
            muscle_bars_html += f"""
            <div class="muscle-bar-container">
                <span class="muscle-label">{muscle}</span>
                <div class="muscle-bar-bg">
                    <div class="muscle-bar-fill" style="width: {percent}%;"></div>
                </div>
                <span class="muscle-percent">{percent}%</span>
            </div>
            """
        
        st.markdown(f"""
        <div class="muscle-chart">
            {muscle_bars_html}
        </div>
        """, unsafe_allow_html=True)
        
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
        
        intensity_bars = ""
        for i in range(5):
            filled_class = "filled" if i < intensity else ""
            high_class = "high" if i >= 3 and i < intensity else ""
            intensity_bars += f'<div class="intensity-bar {filled_class} {high_class}"></div>'
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; padding: 15px; background: rgba(0, 119, 182, 0.05); border-radius: 15px;">
            <div class="intensity-meter">
                {intensity_bars}
            </div>
            <span style="font-family: 'Orbitron', sans-serif; color: #00d4ff; font-size: 1.1rem;">
                {intensity_labels[intensity]}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ===== DETAILED SCHEDULE =====
        st.markdown("### 📋 Detailed Schedule")
        
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
