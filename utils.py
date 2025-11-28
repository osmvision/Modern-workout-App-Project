import pandas as pd
import yt_dlp
import os
import json
from datetime import datetime, timedelta

# Try to import Supabase
try:
    from supabase import create_client, Client
    from config import SUPABASE_URL, SUPABASE_KEY, WORKOUTS_TABLE, CALENDAR_TABLE
    SUPABASE_ENABLED = SUPABASE_KEY != "YOUR_ANON_KEY_HERE" and SUPABASE_KEY != ""
except ImportError:
    SUPABASE_ENABLED = False

# Local file storage (fallback)
DB_FILE = 'workouts.csv'
CALENDAR_FILE = 'workout_calendar.json'
PROGRAMS_FILE = 'workout_programs.json'

# Initialize Supabase client
supabase: Client = None
if SUPABASE_ENABLED:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Connected to Supabase!")
    except Exception as e:
        print(f"⚠️ Supabase connection failed: {e}")
        SUPABASE_ENABLED = False

# ============================================
# DATABASE FUNCTIONS (with Supabase support)
# ============================================

def init_db():
    """Initialize the database"""
    if SUPABASE_ENABLED:
        # Supabase tables should be created via dashboard
        pass
    else:
        if not os.path.exists(DB_FILE):
            df = pd.DataFrame(columns=['title', 'channel', 'url', 'thumbnail', 'category'])
            df.to_csv(DB_FILE, index=False)

def get_video_info(url):
    """Get Video Details from YouTube"""
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'channel': info.get('uploader', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'url': url
            }
        except Exception:
            return None

def add_workout(url, category):
    """Add a workout video to the database"""
    video_data = get_video_info(url)
    if video_data:
        video_data['category'] = category
        
        if SUPABASE_ENABLED:
            try:
                # Add created_at timestamp for Supabase
                video_data['created_at'] = datetime.now().isoformat()
                supabase.table(WORKOUTS_TABLE).insert(video_data).execute()
                return True
            except Exception as e:
                print(f"Supabase error: {e}")
                return False
        else:
            init_db()
            df = pd.read_csv(DB_FILE)
            new_row = pd.DataFrame([video_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            return True
    return False

def get_workouts():
    """Load all workouts from database"""
    if SUPABASE_ENABLED:
        try:
            response = supabase.table(WORKOUTS_TABLE).select("*").order('created_at', desc=True).execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame(columns=['title', 'channel', 'url', 'thumbnail', 'category'])
        except Exception as e:
            print(f"Supabase error: {e}")
            return pd.DataFrame(columns=['title', 'channel', 'url', 'thumbnail', 'category'])
    else:
        init_db()
        return pd.read_csv(DB_FILE)

def delete_workout(workout_id):
    """Delete a workout from database"""
    if SUPABASE_ENABLED:
        try:
            supabase.table(WORKOUTS_TABLE).delete().eq('id', workout_id).execute()
            return True
        except Exception as e:
            print(f"Supabase error: {e}")
            return False
    return False

# ============================================
# PRE-POPULATED WORKOUT VIDEOS
# ============================================

# Curated collection of popular women's workout videos
CURATED_WORKOUT_VIDEOS = [
    {
        'title': '30 MIN FULL BODY WORKOUT - No Equipment',
        'channel': 'Pamela Reif',
        'url': 'https://www.youtube.com/watch?v=UItWltVZZmE',
        'thumbnail': 'https://i.ytimg.com/vi/UItWltVZZmE/maxresdefault.jpg',
        'category': 'HIIT'
    },
    {
        'title': '20 MIN FULL BODY STRETCH - Flexibility & Mobility',
        'channel': 'MadFit',
        'url': 'https://www.youtube.com/watch?v=g_tea8ZNk5A',
        'thumbnail': 'https://i.ytimg.com/vi/g_tea8ZNk5A/maxresdefault.jpg',
        'category': 'Stretching'
    },
    {
        'title': '15 Min Beginner Pilates Workout | Full Body',
        'channel': 'Move With Nicole',
        'url': 'https://www.youtube.com/watch?v=K56Z12XNQ5c',
        'thumbnail': 'https://i.ytimg.com/vi/K56Z12XNQ5c/maxresdefault.jpg',
        'category': 'Pilates'
    },
    {
        'title': '30 Min Yoga Flow | Full Body Stretch',
        'channel': 'Yoga With Adriene',
        'url': 'https://www.youtube.com/watch?v=oBu-pQG6sTY',
        'thumbnail': 'https://i.ytimg.com/vi/oBu-pQG6sTY/maxresdefault.jpg',
        'category': 'Yoga'
    },
    {
        'title': '25 MIN BOOTY WORKOUT - Grow Your Glutes',
        'channel': 'Chloe Ting',
        'url': 'https://www.youtube.com/watch?v=ZYxAHoOweGk',
        'thumbnail': 'https://i.ytimg.com/vi/ZYxAHoOweGk/maxresdefault.jpg',
        'category': 'Strength'
    },
    {
        'title': '15 MIN FAT BURNING HIIT - No Equipment',
        'channel': 'THENX',
        'url': 'https://www.youtube.com/watch?v=ml6cT4AZdqI',
        'thumbnail': 'https://i.ytimg.com/vi/ml6cT4AZdqI/maxresdefault.jpg',
        'category': 'HIIT'
    },
    {
        'title': 'DANCE PARTY WORKOUT - Fun Cardio',
        'channel': 'The Fitness Marshall',
        'url': 'https://www.youtube.com/watch?v=YO0E9J-LlEE',
        'thumbnail': 'https://i.ytimg.com/vi/YO0E9J-LlEE/maxresdefault.jpg',
        'category': 'Dance'
    },
    {
        'title': '20 Min Abs Workout - Core Strengthening',
        'channel': 'Blogilates',
        'url': 'https://www.youtube.com/watch?v=9p7-YC91Q74',
        'thumbnail': 'https://i.ytimg.com/vi/9p7-YC91Q74/maxresdefault.jpg',
        'category': 'Strength'
    },
    {
        'title': '30 MIN WALKING WORKOUT - Fat Burning Indoor Walk',
        'channel': 'growwithjo',
        'url': 'https://www.youtube.com/watch?v=5WzKKrFwUGQ',
        'thumbnail': 'https://i.ytimg.com/vi/5WzKKrFwUGQ/maxresdefault.jpg',
        'category': 'Cardio'
    },
    {
        'title': '10 MIN MORNING YOGA STRETCH',
        'channel': 'Sarah Beth Yoga',
        'url': 'https://www.youtube.com/watch?v=4pKly2JojMw',
        'thumbnail': 'https://i.ytimg.com/vi/4pKly2JojMw/maxresdefault.jpg',
        'category': 'Yoga'
    },
    {
        'title': '20 MIN UPPER BODY WORKOUT - Toned Arms',
        'channel': 'Sydney Cummings',
        'url': 'https://www.youtube.com/watch?v=5kOLRmgfNvM',
        'thumbnail': 'https://i.ytimg.com/vi/5kOLRmgfNvM/maxresdefault.jpg',
        'category': 'Strength'
    },
    {
        'title': '15 MIN LEG WORKOUT - Slim Thighs',
        'channel': 'Lilly Sabri',
        'url': 'https://www.youtube.com/watch?v=XF5clnw4QOM',
        'thumbnail': 'https://i.ytimg.com/vi/XF5clnw4QOM/maxresdefault.jpg',
        'category': 'Strength'
    }
]

def get_starter_videos():
    """Get the curated starter workout videos"""
    return CURATED_WORKOUT_VIDEOS

def seed_starter_videos():
    """Seed the database with starter videos if empty"""
    df = get_workouts()
    if df.empty:
        for video in CURATED_WORKOUT_VIDEOS:
            if SUPABASE_ENABLED:
                try:
                    video_data = video.copy()
                    video_data['created_at'] = datetime.now().isoformat()
                    supabase.table(WORKOUTS_TABLE).insert(video_data).execute()
                except Exception as e:
                    print(f"Error seeding video: {e}")
            else:
                init_db()
                df = pd.read_csv(DB_FILE)
                new_row = pd.DataFrame([video])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
        return True
    return False

# ============================================
# CALENDAR FUNCTIONS (with Supabase support)
# ============================================

def init_calendar():
    """Initialize the calendar"""
    if SUPABASE_ENABLED:
        pass  # Tables created via Supabase dashboard
    else:
        if not os.path.exists(CALENDAR_FILE):
            save_calendar({})
    return load_calendar()

def load_calendar():
    """Load calendar data"""
    if SUPABASE_ENABLED:
        try:
            response = supabase.table(CALENDAR_TABLE).select("*").execute()
            calendar_data = {}
            for row in response.data:
                date_str = row['date']
                if date_str not in calendar_data:
                    calendar_data[date_str] = []
                calendar_data[date_str].append({
                    'id': row['id'],
                    'name': row['name'],
                    'type': row['type'],
                    'duration': row['duration'],
                    'notes': row.get('notes', ''),
                    'completed': row.get('completed', False)
                })
            return calendar_data
        except Exception as e:
            print(f"Supabase error: {e}")
            return {}
    else:
        try:
            with open(CALENDAR_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

def save_calendar(calendar_data):
    """Save calendar data (local only)"""
    if not SUPABASE_ENABLED:
        with open(CALENDAR_FILE, 'w') as f:
            json.dump(calendar_data, f, indent=2)

def add_workout_to_calendar(date_str, workout_data):
    """Add a workout to a specific date"""
    if SUPABASE_ENABLED:
        try:
            data = {
                'date': date_str,
                'name': workout_data.get('name', ''),
                'type': workout_data.get('type', ''),
                'duration': workout_data.get('duration', ''),
                'notes': workout_data.get('notes', ''),
                'completed': workout_data.get('completed', False)
            }
            supabase.table(CALENDAR_TABLE).insert(data).execute()
            return True
        except Exception as e:
            print(f"Supabase error: {e}")
            return False
    else:
        calendar = load_calendar()
        if date_str not in calendar:
            calendar[date_str] = []
        calendar[date_str].append(workout_data)
        save_calendar(calendar)
        return True

def update_workout_in_calendar(date_str, workout_index, workout_data):
    """Update a specific workout on a date"""
    if SUPABASE_ENABLED:
        try:
            calendar = load_calendar()
            if date_str in calendar and workout_index < len(calendar[date_str]):
                workout_id = calendar[date_str][workout_index].get('id')
                if workout_id:
                    supabase.table(CALENDAR_TABLE).update(workout_data).eq('id', workout_id).execute()
        except Exception as e:
            print(f"Supabase error: {e}")
    else:
        calendar = load_calendar()
        if date_str in calendar and workout_index < len(calendar[date_str]):
            calendar[date_str][workout_index] = workout_data
            save_calendar(calendar)

def remove_workout_from_calendar(date_str, workout_index):
    """Remove a workout from a specific date"""
    if SUPABASE_ENABLED:
        try:
            calendar = load_calendar()
            if date_str in calendar and workout_index < len(calendar[date_str]):
                workout_id = calendar[date_str][workout_index].get('id')
                if workout_id:
                    supabase.table(CALENDAR_TABLE).delete().eq('id', workout_id).execute()
        except Exception as e:
            print(f"Supabase error: {e}")
    else:
        calendar = load_calendar()
        if date_str in calendar and workout_index < len(calendar[date_str]):
            calendar[date_str].pop(workout_index)
            if not calendar[date_str]:
                del calendar[date_str]
            save_calendar(calendar)

def get_workouts_for_date(date_str):
    """Get all workouts for a specific date"""
    if SUPABASE_ENABLED:
        try:
            response = supabase.table(CALENDAR_TABLE).select("*").eq('date', date_str).execute()
            return [{
                'id': row['id'],
                'name': row['name'],
                'type': row['type'],
                'duration': row['duration'],
                'notes': row.get('notes', ''),
                'completed': row.get('completed', False)
            } for row in response.data]
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    else:
        calendar = load_calendar()
        return calendar.get(date_str, [])

def mark_workout_complete(date_str, workout_index, completed=True):
    """Mark a workout as complete/incomplete"""
    if SUPABASE_ENABLED:
        try:
            calendar = load_calendar()
            if date_str in calendar and workout_index < len(calendar[date_str]):
                workout_id = calendar[date_str][workout_index].get('id')
                if workout_id:
                    supabase.table(CALENDAR_TABLE).update({'completed': completed}).eq('id', workout_id).execute()
        except Exception as e:
            print(f"Supabase error: {e}")
    else:
        calendar = load_calendar()
        if date_str in calendar and workout_index < len(calendar[date_str]):
            calendar[date_str][workout_index]['completed'] = completed
            save_calendar(calendar)

# ============================================
# WORKOUT PROGRAMS FOR WOMEN
# ============================================

GIRLS_WORKOUT_PROGRAMS = {
    "beginner_full_body": {
        "name": "💪 Beginner Full Body Tone",
        "description": "Perfect for beginners! A gentle introduction to fitness with full body workouts.",
        "duration": "4 weeks",
        "level": "Beginner",
        "goal": "Tone & Build Foundation",
        "days_per_week": 3,
        "schedule": {
            "Week 1-2": {
                "Day 1": {
                    "focus": "Lower Body",
                    "exercises": [
                        {"name": "Bodyweight Squats", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Glute Bridges", "sets": 3, "reps": "15", "rest": "45s"},
                        {"name": "Lunges (each leg)", "sets": 2, "reps": "10", "rest": "45s"},
                        {"name": "Calf Raises", "sets": 3, "reps": "15", "rest": "30s"},
                        {"name": "Wall Sit", "sets": 2, "reps": "30s hold", "rest": "45s"},
                    ]
                },
                "Day 2": {
                    "focus": "Upper Body & Core",
                    "exercises": [
                        {"name": "Wall Push-ups", "sets": 3, "reps": "10", "rest": "45s"},
                        {"name": "Arm Circles", "sets": 2, "reps": "30s each direction", "rest": "30s"},
                        {"name": "Plank Hold", "sets": 3, "reps": "20s", "rest": "45s"},
                        {"name": "Bird Dogs", "sets": 2, "reps": "10 each side", "rest": "45s"},
                        {"name": "Dead Bug", "sets": 3, "reps": "10 each side", "rest": "45s"},
                    ]
                },
                "Day 3": {
                    "focus": "Full Body & Cardio",
                    "exercises": [
                        {"name": "Jumping Jacks", "sets": 3, "reps": "30s", "rest": "30s"},
                        {"name": "Squat to Calf Raise", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Incline Push-ups", "sets": 2, "reps": "8", "rest": "45s"},
                        {"name": "Standing Oblique Crunches", "sets": 2, "reps": "12 each side", "rest": "45s"},
                        {"name": "March in Place", "sets": 3, "reps": "45s", "rest": "30s"},
                    ]
                }
            },
            "Week 3-4": {
                "Day 1": {
                    "focus": "Lower Body Progression",
                    "exercises": [
                        {"name": "Sumo Squats", "sets": 3, "reps": "15", "rest": "45s"},
                        {"name": "Single Leg Glute Bridges", "sets": 3, "reps": "10 each", "rest": "45s"},
                        {"name": "Reverse Lunges", "sets": 3, "reps": "10 each", "rest": "45s"},
                        {"name": "Fire Hydrants", "sets": 3, "reps": "12 each", "rest": "30s"},
                        {"name": "Donkey Kicks", "sets": 3, "reps": "12 each", "rest": "30s"},
                    ]
                },
                "Day 2": {
                    "focus": "Upper Body & Core Progression",
                    "exercises": [
                        {"name": "Knee Push-ups", "sets": 3, "reps": "10", "rest": "45s"},
                        {"name": "Tricep Dips (chair)", "sets": 3, "reps": "10", "rest": "45s"},
                        {"name": "Plank Hold", "sets": 3, "reps": "30s", "rest": "45s"},
                        {"name": "Bicycle Crunches", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "Superman Hold", "sets": 3, "reps": "20s", "rest": "45s"},
                    ]
                },
                "Day 3": {
                    "focus": "Full Body HIIT Light",
                    "exercises": [
                        {"name": "High Knees", "sets": 3, "reps": "30s", "rest": "30s"},
                        {"name": "Squat Pulses", "sets": 3, "reps": "15", "rest": "45s"},
                        {"name": "Push-up to Shoulder Tap", "sets": 2, "reps": "8", "rest": "45s"},
                        {"name": "Mountain Climbers (slow)", "sets": 3, "reps": "20s", "rest": "45s"},
                        {"name": "Cool Down Stretch", "sets": 1, "reps": "3 min", "rest": ""},
                    ]
                }
            }
        }
    },
    "slim_thick": {
        "name": "🍑 Slim Thick Program",
        "description": "Build curves in all the right places! Focus on glutes, thighs, and a tiny waist.",
        "duration": "6 weeks",
        "level": "Intermediate",
        "goal": "Build Glutes & Slim Waist",
        "days_per_week": 4,
        "schedule": {
            "Week 1-3": {
                "Day 1": {
                    "focus": "🍑 Glute Focus",
                    "exercises": [
                        {"name": "Hip Thrusts", "sets": 4, "reps": "15", "rest": "60s"},
                        {"name": "Sumo Squats", "sets": 4, "reps": "12", "rest": "60s"},
                        {"name": "Romanian Deadlifts", "sets": 3, "reps": "12", "rest": "60s"},
                        {"name": "Cable Kickbacks", "sets": 3, "reps": "15 each", "rest": "45s"},
                        {"name": "Frog Pumps", "sets": 3, "reps": "20", "rest": "45s"},
                    ]
                },
                "Day 2": {
                    "focus": "👙 Waist & Core",
                    "exercises": [
                        {"name": "Vacuum Exercise", "sets": 3, "reps": "30s hold", "rest": "30s"},
                        {"name": "Side Plank", "sets": 3, "reps": "30s each", "rest": "30s"},
                        {"name": "Russian Twists", "sets": 3, "reps": "20", "rest": "45s"},
                        {"name": "Leg Raises", "sets": 3, "reps": "15", "rest": "45s"},
                        {"name": "Dead Bug", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "20 min LISS Cardio", "sets": 1, "reps": "20 min", "rest": ""},
                    ]
                },
                "Day 3": {
                    "focus": "🦵 Legs & Glutes",
                    "exercises": [
                        {"name": "Bulgarian Split Squats", "sets": 3, "reps": "12 each", "rest": "60s"},
                        {"name": "Goblet Squats", "sets": 4, "reps": "12", "rest": "60s"},
                        {"name": "Good Mornings", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Curtsy Lunges", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "Clamshells", "sets": 3, "reps": "15 each", "rest": "30s"},
                    ]
                },
                "Day 4": {
                    "focus": "💪 Upper Body Tone",
                    "exercises": [
                        {"name": "Push-ups", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Dumbbell Rows", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "Shoulder Press", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Tricep Dips", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Bicep Curls", "sets": 3, "reps": "12", "rest": "45s"},
                    ]
                }
            },
            "Week 4-6": {
                "Day 1": {
                    "focus": "🍑 Advanced Glute",
                    "exercises": [
                        {"name": "Barbell Hip Thrusts", "sets": 4, "reps": "12", "rest": "90s"},
                        {"name": "Deficit Sumo Squats", "sets": 4, "reps": "10", "rest": "90s"},
                        {"name": "Single Leg RDL", "sets": 3, "reps": "10 each", "rest": "60s"},
                        {"name": "Cable Pull-Through", "sets": 3, "reps": "15", "rest": "45s"},
                        {"name": "Banded Glute Bridges", "sets": 3, "reps": "20", "rest": "45s"},
                    ]
                },
                "Day 2": {
                    "focus": "👙 Core & HIIT",
                    "exercises": [
                        {"name": "Plank Variations Circuit", "sets": 3, "reps": "45s each", "rest": "30s"},
                        {"name": "Woodchoppers", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "Hanging Leg Raises", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Ab Wheel Rollouts", "sets": 3, "reps": "10", "rest": "45s"},
                        {"name": "HIIT Sprints", "sets": 8, "reps": "30s on/30s off", "rest": ""},
                    ]
                },
                "Day 3": {
                    "focus": "🦵 Leg Sculptor",
                    "exercises": [
                        {"name": "Front Squats", "sets": 4, "reps": "10", "rest": "90s"},
                        {"name": "Walking Lunges", "sets": 3, "reps": "12 each", "rest": "60s"},
                        {"name": "Leg Press", "sets": 4, "reps": "12", "rest": "60s"},
                        {"name": "Leg Curls", "sets": 3, "reps": "15", "rest": "45s"},
                        {"name": "Calf Raises", "sets": 4, "reps": "20", "rest": "30s"},
                    ]
                },
                "Day 4": {
                    "focus": "💪 Toned Arms",
                    "exercises": [
                        {"name": "Diamond Push-ups", "sets": 3, "reps": "10", "rest": "45s"},
                        {"name": "Lat Pulldowns", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Arnold Press", "sets": 3, "reps": "10", "rest": "45s"},
                        {"name": "Skull Crushers", "sets": 3, "reps": "12", "rest": "45s"},
                        {"name": "Hammer Curls", "sets": 3, "reps": "12", "rest": "45s"},
                    ]
                }
            }
        }
    },
    "yoga_flexibility": {
        "name": "🧘 Yoga & Flexibility Flow",
        "description": "Increase flexibility, reduce stress, and find your inner peace with daily yoga.",
        "duration": "4 weeks",
        "level": "All Levels",
        "goal": "Flexibility & Mindfulness",
        "days_per_week": 5,
        "schedule": {
            "Week 1-4": {
                "Day 1": {
                    "focus": "🌅 Morning Sun Salutation",
                    "exercises": [
                        {"name": "Mountain Pose", "sets": 1, "reps": "5 breaths", "rest": ""},
                        {"name": "Forward Fold", "sets": 1, "reps": "5 breaths", "rest": ""},
                        {"name": "Halfway Lift", "sets": 1, "reps": "3 breaths", "rest": ""},
                        {"name": "Plank to Chaturanga", "sets": 1, "reps": "3 breaths", "rest": ""},
                        {"name": "Upward Dog", "sets": 1, "reps": "3 breaths", "rest": ""},
                        {"name": "Downward Dog", "sets": 1, "reps": "5 breaths", "rest": ""},
                        {"name": "Repeat Sun Salutation", "sets": 5, "reps": "full flow", "rest": ""},
                    ]
                },
                "Day 2": {
                    "focus": "🦵 Hip Opening Flow",
                    "exercises": [
                        {"name": "Butterfly Pose", "sets": 1, "reps": "2 min", "rest": ""},
                        {"name": "Pigeon Pose (each side)", "sets": 1, "reps": "2 min", "rest": ""},
                        {"name": "Frog Pose", "sets": 1, "reps": "2 min", "rest": ""},
                        {"name": "Happy Baby", "sets": 1, "reps": "1 min", "rest": ""},
                        {"name": "Reclined Twist", "sets": 1, "reps": "1 min each", "rest": ""},
                    ]
                },
                "Day 3": {
                    "focus": "💪 Strength Yoga",
                    "exercises": [
                        {"name": "Chair Pose Hold", "sets": 3, "reps": "30s", "rest": "15s"},
                        {"name": "Warrior I", "sets": 2, "reps": "45s each", "rest": ""},
                        {"name": "Warrior II", "sets": 2, "reps": "45s each", "rest": ""},
                        {"name": "Warrior III", "sets": 2, "reps": "30s each", "rest": ""},
                        {"name": "Boat Pose", "sets": 3, "reps": "30s", "rest": "15s"},
                        {"name": "Crow Pose Practice", "sets": 5, "reps": "attempts", "rest": ""},
                    ]
                },
                "Day 4": {
                    "focus": "🌙 Relaxation & Restore",
                    "exercises": [
                        {"name": "Child's Pose", "sets": 1, "reps": "3 min", "rest": ""},
                        {"name": "Legs Up Wall", "sets": 1, "reps": "5 min", "rest": ""},
                        {"name": "Supported Bridge", "sets": 1, "reps": "3 min", "rest": ""},
                        {"name": "Supine Twist", "sets": 1, "reps": "2 min each", "rest": ""},
                        {"name": "Savasana", "sets": 1, "reps": "10 min", "rest": ""},
                    ]
                },
                "Day 5": {
                    "focus": "🔥 Power Yoga Flow",
                    "exercises": [
                        {"name": "Dynamic Sun Salutation A", "sets": 5, "reps": "flow", "rest": ""},
                        {"name": "Sun Salutation B", "sets": 5, "reps": "flow", "rest": ""},
                        {"name": "Standing Balance Series", "sets": 1, "reps": "5 min", "rest": ""},
                        {"name": "Core Flow", "sets": 1, "reps": "5 min", "rest": ""},
                        {"name": "Cool Down", "sets": 1, "reps": "5 min", "rest": ""},
                    ]
                }
            }
        }
    },
    "hiit_fat_burn": {
        "name": "🔥 HIIT Fat Burner",
        "description": "High intensity workouts to maximize calorie burn and boost metabolism!",
        "duration": "4 weeks",
        "level": "Intermediate-Advanced",
        "goal": "Fat Loss & Endurance",
        "days_per_week": 4,
        "schedule": {
            "Week 1-2": {
                "Day 1": {
                    "focus": "⚡ Full Body HIIT",
                    "exercises": [
                        {"name": "Burpees", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Jump Squats", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Mountain Climbers", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "High Knees", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Plank Jacks", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                    ]
                },
                "Day 2": {
                    "focus": "🦵 Lower Body HIIT",
                    "exercises": [
                        {"name": "Jump Lunges", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Squat Jumps", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Skaters", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Box Jumps/Step Ups", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Wall Sit", "sets": 3, "reps": "45s", "rest": "15s"},
                    ]
                },
                "Day 3": {
                    "focus": "💪 Upper Body HIIT",
                    "exercises": [
                        {"name": "Push-up Variations", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Plank Up-Downs", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Tricep Dips Fast", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Shoulder Taps", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Inchworms", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                    ]
                },
                "Day 4": {
                    "focus": "🎯 Core HIIT",
                    "exercises": [
                        {"name": "Bicycle Crunches", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "V-Ups", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Plank to Pike", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Russian Twists", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                        {"name": "Dead Bug Fast", "sets": 4, "reps": "30s on/30s off", "rest": ""},
                    ]
                }
            },
            "Week 3-4": {
                "Day 1": {
                    "focus": "⚡ Tabata Full Body",
                    "exercises": [
                        {"name": "Tabata Burpees", "sets": 8, "reps": "20s on/10s off", "rest": "1 min after"},
                        {"name": "Tabata Squats", "sets": 8, "reps": "20s on/10s off", "rest": "1 min after"},
                        {"name": "Tabata Push-ups", "sets": 8, "reps": "20s on/10s off", "rest": "1 min after"},
                        {"name": "Tabata Abs", "sets": 8, "reps": "20s on/10s off", "rest": ""},
                    ]
                },
                "Day 2": {
                    "focus": "🦵 Leg Tabata",
                    "exercises": [
                        {"name": "Tabata Jump Lunges", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Sumo Squats", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Glute Bridges", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Calf Raises", "sets": 8, "reps": "20s on/10s off", "rest": ""},
                    ]
                },
                "Day 3": {
                    "focus": "💪 Upper Tabata",
                    "exercises": [
                        {"name": "Tabata Diamond Push-ups", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Pike Push-ups", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Plank Hold", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Burpees", "sets": 8, "reps": "20s on/10s off", "rest": ""},
                    ]
                },
                "Day 4": {
                    "focus": "🎯 Core Destroyer",
                    "exercises": [
                        {"name": "Tabata Leg Raises", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Mountain Climbers", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Plank Jacks", "sets": 8, "reps": "20s on/10s off", "rest": "1 min"},
                        {"name": "Tabata Flutter Kicks", "sets": 8, "reps": "20s on/10s off", "rest": ""},
                    ]
                }
            }
        }
    },
    "booty_builder": {
        "name": "🍑 30 Day Booty Builder",
        "description": "Sculpt and lift your glutes with this targeted 30-day challenge!",
        "duration": "30 days",
        "level": "All Levels",
        "goal": "Glute Growth & Shape",
        "days_per_week": 6,
        "schedule": {
            "Week 1": {
                "Day 1": {
                    "focus": "🍑 Glute Activation",
                    "exercises": [
                        {"name": "Glute Bridges", "sets": 3, "reps": "20", "rest": "30s"},
                        {"name": "Donkey Kicks", "sets": 3, "reps": "15 each", "rest": "30s"},
                        {"name": "Fire Hydrants", "sets": 3, "reps": "15 each", "rest": "30s"},
                        {"name": "Clamshells", "sets": 3, "reps": "15 each", "rest": "30s"},
                    ]
                },
                "Day 2": {
                    "focus": "🦵 Squat Day",
                    "exercises": [
                        {"name": "Bodyweight Squats", "sets": 4, "reps": "15", "rest": "45s"},
                        {"name": "Sumo Squats", "sets": 3, "reps": "15", "rest": "45s"},
                        {"name": "Pulse Squats", "sets": 3, "reps": "20", "rest": "45s"},
                        {"name": "Squat Hold", "sets": 3, "reps": "30s", "rest": "30s"},
                    ]
                },
                "Day 3": {
                    "focus": "🍑 Hip Thrust Focus",
                    "exercises": [
                        {"name": "Hip Thrusts", "sets": 4, "reps": "15", "rest": "45s"},
                        {"name": "Single Leg Hip Thrust", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "Frog Pumps", "sets": 3, "reps": "20", "rest": "30s"},
                        {"name": "Glute Squeeze Hold", "sets": 3, "reps": "30s", "rest": "30s"},
                    ]
                },
                "Day 4": {
                    "focus": "🦵 Lunge Day",
                    "exercises": [
                        {"name": "Forward Lunges", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "Reverse Lunges", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "Curtsy Lunges", "sets": 3, "reps": "12 each", "rest": "45s"},
                        {"name": "Walking Lunges", "sets": 3, "reps": "10 each", "rest": "45s"},
                    ]
                },
                "Day 5": {
                    "focus": "🍑 Kickback Day",
                    "exercises": [
                        {"name": "Standing Kickbacks", "sets": 3, "reps": "15 each", "rest": "30s"},
                        {"name": "Quadruped Kickbacks", "sets": 3, "reps": "15 each", "rest": "30s"},
                        {"name": "Pulse Kickbacks", "sets": 3, "reps": "20 each", "rest": "30s"},
                        {"name": "Rainbow Kicks", "sets": 3, "reps": "12 each", "rest": "30s"},
                    ]
                },
                "Day 6": {
                    "focus": "🔥 Burnout Day",
                    "exercises": [
                        {"name": "Glute Bridge Burnout", "sets": 1, "reps": "100", "rest": ""},
                        {"name": "Squat Burnout", "sets": 1, "reps": "50", "rest": ""},
                        {"name": "Donkey Kick Burnout", "sets": 1, "reps": "30 each", "rest": ""},
                        {"name": "Wall Sit Burnout", "sets": 1, "reps": "2 min", "rest": ""},
                    ]
                }
            }
        }
    }
}

def get_workout_programs():
    """Return all available workout programs"""
    return GIRLS_WORKOUT_PROGRAMS

def get_program_by_id(program_id):
    """Get a specific program by its ID"""
    return GIRLS_WORKOUT_PROGRAMS.get(program_id)