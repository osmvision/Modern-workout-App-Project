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
            # Try ordering by created_at, fallback to no ordering if column doesn't exist
            try:
                response = supabase.table(WORKOUTS_TABLE).select("*").order('created_at', desc=True).execute()
            except:
                response = supabase.table(WORKOUTS_TABLE).select("*").execute()
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

def clear_calendar():
    """Clear all workouts from the calendar"""
    if SUPABASE_ENABLED:
        try:
            # Delete all records from calendar table
            supabase.table(CALENDAR_TABLE).delete().neq('id', 0).execute()
            return True
        except Exception as e:
            print(f"Supabase error clearing calendar: {e}")
            return False
    else:
        save_calendar({})
        return True

def init_calendar():
    """Initialize the calendar"""
    if SUPABASE_ENABLED:
        pass  # Tables created via Supabase dashboard
    else:
        if not os.path.exists(CALENDAR_FILE):
            save_calendar({})
    return load_calendar()

def populate_sample_workouts():
    """Create a comprehensive ONE-YEAR workout calendar with progressive training"""
    from datetime import datetime, timedelta
    import random
    
    calendar = load_calendar()
    
    # Only populate if calendar is empty
    if calendar:
        return False
    
    today = datetime.now().date()
    
    # ===== COMPREHENSIVE WORKOUT LIBRARY =====
    
    # Lower Body Workouts (Progressive)
    lower_body_beginner = [
        {"name": "Bodyweight Squats & Lunges", "type": "Lower Body", "duration": "25 min", "notes": "3x12 squats, 3x10 lunges each leg"},
        {"name": "Glute Bridges & Kickbacks", "type": "Lower Body", "duration": "20 min", "notes": "3x15 bridges, 3x12 kickbacks"},
        {"name": "Wall Sits & Calf Raises", "type": "Lower Body", "duration": "20 min", "notes": "3x30sec wall sit, 3x20 calf raises"},
    ]
    
    lower_body_intermediate = [
        {"name": "Sumo Squats & Romanian Deadlifts", "type": "Lower Body", "duration": "35 min", "notes": "4x12 sumo squats, 4x10 RDL with weights"},
        {"name": "Bulgarian Split Squats", "type": "Lower Body", "duration": "30 min", "notes": "4x10 each leg, add weights"},
        {"name": "Hip Thrusts & Step Ups", "type": "Lower Body", "duration": "35 min", "notes": "4x15 hip thrusts, 3x12 step ups"},
        {"name": "Goblet Squats & Leg Press", "type": "Lower Body", "duration": "40 min", "notes": "4x12 goblet, 4x15 leg press"},
    ]
    
    lower_body_advanced = [
        {"name": "Barbell Squats & Deadlifts", "type": "Lower Body", "duration": "50 min", "notes": "5x5 squats, 5x5 deadlifts - heavy"},
        {"name": "Power Leg Day", "type": "Lower Body", "duration": "55 min", "notes": "Jump squats, box jumps, weighted lunges"},
        {"name": "Glute Destroyer", "type": "Lower Body", "duration": "45 min", "notes": "Heavy hip thrusts, sumo deads, cable kickbacks"},
        {"name": "Quad & Ham Focus", "type": "Lower Body", "duration": "50 min", "notes": "Front squats, leg curls, leg extensions"},
    ]
    
    # Upper Body Workouts (Progressive)
    upper_body_beginner = [
        {"name": "Push-ups & Arm Circles", "type": "Upper Body", "duration": "20 min", "notes": "Modified push-ups 3x8, arm mobility"},
        {"name": "Tricep Dips & Wall Push-ups", "type": "Upper Body", "duration": "20 min", "notes": "Chair dips 3x10, wall push 3x12"},
        {"name": "Resistance Band Arms", "type": "Upper Body", "duration": "25 min", "notes": "Band curls, band rows, band presses"},
    ]
    
    upper_body_intermediate = [
        {"name": "Dumbbell Chest & Back", "type": "Upper Body", "duration": "35 min", "notes": "DB press 4x10, rows 4x12, flyes 3x12"},
        {"name": "Shoulder Sculpt", "type": "Upper Body", "duration": "30 min", "notes": "OHP 4x10, lateral raises 4x12, rear delts"},
        {"name": "Biceps & Triceps Tone", "type": "Upper Body", "duration": "30 min", "notes": "Curls 4x12, tricep extensions 4x12"},
        {"name": "Push-Pull Combo", "type": "Upper Body", "duration": "40 min", "notes": "Push-ups, rows, shoulder press circuit"},
    ]
    
    upper_body_advanced = [
        {"name": "Heavy Push Day", "type": "Upper Body", "duration": "50 min", "notes": "Bench 5x5, incline DB, dips, tricep work"},
        {"name": "Heavy Pull Day", "type": "Upper Body", "duration": "50 min", "notes": "Pull-ups, barbell rows, face pulls, curls"},
        {"name": "Shoulder Power", "type": "Upper Body", "duration": "45 min", "notes": "Military press 5x5, Arnold press, raises"},
        {"name": "Arm Blast", "type": "Upper Body", "duration": "40 min", "notes": "Supersets: curls + triceps, 21s, drop sets"},
    ]
    
    # Core Workouts (Progressive)
    core_beginner = [
        {"name": "Basic Core Work", "type": "Core", "duration": "15 min", "notes": "Crunches, dead bugs, bird dogs"},
        {"name": "Plank Challenge", "type": "Core", "duration": "15 min", "notes": "Plank holds, side planks, knee tucks"},
    ]
    
    core_intermediate = [
        {"name": "Ab Burner", "type": "Core", "duration": "20 min", "notes": "Bicycle crunches, leg raises, Russian twists"},
        {"name": "Core Stability", "type": "Core", "duration": "25 min", "notes": "Plank variations, hollow holds, mountain climbers"},
        {"name": "Pilates Core", "type": "Core", "duration": "30 min", "notes": "Hundred, scissors, roll-ups, teaser"},
    ]
    
    core_advanced = [
        {"name": "Intense Ab Circuit", "type": "Core", "duration": "25 min", "notes": "Hanging leg raises, ab wheel, weighted crunches"},
        {"name": "Functional Core", "type": "Core", "duration": "30 min", "notes": "Turkish get-ups, windmills, loaded carries"},
    ]
    
    # HIIT Workouts (Progressive)
    hiit_beginner = [
        {"name": "Beginner HIIT", "type": "HIIT", "duration": "20 min", "notes": "30s work/30s rest - squats, jacks, marching"},
        {"name": "Low Impact HIIT", "type": "HIIT", "duration": "25 min", "notes": "Step touches, modified burpees, knee lifts"},
    ]
    
    hiit_intermediate = [
        {"name": "Tabata Burn", "type": "HIIT", "duration": "30 min", "notes": "20s on/10s off x 8 rounds, multiple exercises"},
        {"name": "EMOM Challenge", "type": "HIIT", "duration": "30 min", "notes": "Every minute: 10 burpees, 15 squats"},
        {"name": "Cardio HIIT", "type": "HIIT", "duration": "35 min", "notes": "High knees, burpees, jump lunges, mountain climbers"},
    ]
    
    hiit_advanced = [
        {"name": "Extreme HIIT", "type": "HIIT", "duration": "40 min", "notes": "45s work/15s rest - plyometrics, burpees, sprints"},
        {"name": "MetCon Madness", "type": "HIIT", "duration": "45 min", "notes": "Metabolic conditioning: AMRAPs and EMOMs"},
        {"name": "Warrior HIIT", "type": "HIIT", "duration": "40 min", "notes": "Battle ropes, box jumps, kettlebell swings"},
    ]
    
    # Full Body Workouts (Progressive)
    full_body_beginner = [
        {"name": "Full Body Basics", "type": "Full Body", "duration": "30 min", "notes": "Squats, push-ups, lunges, planks"},
        {"name": "Total Body Tone", "type": "Full Body", "duration": "30 min", "notes": "Light weights, 3 rounds full body circuit"},
    ]
    
    full_body_intermediate = [
        {"name": "Full Body Strength", "type": "Full Body", "duration": "45 min", "notes": "Compound movements: squat, press, row, lunge"},
        {"name": "Circuit Training", "type": "Full Body", "duration": "40 min", "notes": "5 exercises, 4 rounds, 45s each"},
        {"name": "Dumbbell Full Body", "type": "Full Body", "duration": "45 min", "notes": "Complete workout with dumbbells only"},
    ]
    
    full_body_advanced = [
        {"name": "Power Full Body", "type": "Full Body", "duration": "55 min", "notes": "Olympic lifts, compound movements, plyometrics"},
        {"name": "Athlete Training", "type": "Full Body", "duration": "60 min", "notes": "Sport-specific movements, agility, power"},
        {"name": "CrossFit Style WOD", "type": "Full Body", "duration": "50 min", "notes": "AMRAP: thrusters, pull-ups, box jumps, row"},
    ]
    
    # Cardio Workouts
    cardio_workouts = [
        {"name": "Dance Cardio Party", "type": "Cardio", "duration": "30 min", "notes": "Fun dance moves, choreo combos"},
        {"name": "Walking Workout", "type": "Cardio", "duration": "40 min", "notes": "Power walking with intervals"},
        {"name": "Stair Master", "type": "Cardio", "duration": "30 min", "notes": "Stair climbing intervals"},
        {"name": "Jump Rope Session", "type": "Cardio", "duration": "25 min", "notes": "Intervals: singles, high knees, criss-cross"},
        {"name": "Cycling Sprint", "type": "Cardio", "duration": "35 min", "notes": "Indoor cycling with sprint intervals"},
        {"name": "Rowing Endurance", "type": "Cardio", "duration": "30 min", "notes": "500m intervals, technique focus"},
    ]
    
    # Yoga & Flexibility
    yoga_workouts = [
        {"name": "Morning Sun Salutations", "type": "Yoga", "duration": "20 min", "notes": "5-10 sun salutation flows"},
        {"name": "Vinyasa Flow", "type": "Yoga", "duration": "45 min", "notes": "Dynamic flow with breath"},
        {"name": "Power Yoga", "type": "Yoga", "duration": "50 min", "notes": "Strength-building yoga poses"},
        {"name": "Yin Yoga", "type": "Yoga", "duration": "45 min", "notes": "Deep stretches, 3-5 min holds"},
        {"name": "Hip Opening Yoga", "type": "Yoga", "duration": "35 min", "notes": "Focus on hip flexibility"},
        {"name": "Yoga for Athletes", "type": "Yoga", "duration": "40 min", "notes": "Recovery-focused stretches"},
    ]
    
    # Pilates
    pilates_workouts = [
        {"name": "Mat Pilates Basics", "type": "Pilates", "duration": "30 min", "notes": "Classic mat exercises"},
        {"name": "Pilates Abs Focus", "type": "Pilates", "duration": "25 min", "notes": "Core-intensive Pilates"},
        {"name": "Pilates Sculpt", "type": "Pilates", "duration": "40 min", "notes": "Full body Pilates with weights"},
        {"name": "Barre Pilates", "type": "Pilates", "duration": "45 min", "notes": "Ballet-inspired movements"},
    ]
    
    # Recovery & Stretching
    recovery_workouts = [
        {"name": "Active Recovery", "type": "Stretching", "duration": "20 min", "notes": "Light movement, foam rolling"},
        {"name": "Deep Stretch", "type": "Stretching", "duration": "30 min", "notes": "Full body stretch sequence"},
        {"name": "Foam Rolling", "type": "Stretching", "duration": "20 min", "notes": "Self-myofascial release"},
        {"name": "Mobility Flow", "type": "Stretching", "duration": "25 min", "notes": "Joint mobility exercises"},
    ]
    
    # ===== GENERATE ONE YEAR OF WORKOUTS =====
    
    def get_phase(week_num):
        """Determine training phase based on week number"""
        if week_num <= 4:
            return "foundation"  # Weeks 1-4: Build habits
        elif week_num <= 12:
            return "beginner"    # Weeks 5-12: Beginner progression
        elif week_num <= 26:
            return "intermediate" # Weeks 13-26: Intermediate
        elif week_num <= 40:
            return "advanced"    # Weeks 27-40: Advanced
        else:
            return "peak"        # Weeks 41-52: Peak performance
    
    def get_workout_for_day(day_of_week, week_num, day_count):
        """Get appropriate workout based on day, week, and training phase"""
        phase = get_phase(week_num)
        
        # Sunday is REST day
        if day_of_week == 6:
            return None
        
        # Workout split based on day of week
        # Monday: Lower Body
        # Tuesday: HIIT/Cardio
        # Wednesday: Upper Body
        # Thursday: Yoga/Pilates (Active Recovery)
        # Friday: Full Body
        # Saturday: Cardio/Fun workout
        
        random.seed(day_count)  # Consistent randomization
        
        if day_of_week == 0:  # Monday - Lower Body
            if phase == "foundation":
                return random.choice(lower_body_beginner)
            elif phase == "beginner":
                return random.choice(lower_body_beginner + lower_body_intermediate[:1])
            elif phase == "intermediate":
                return random.choice(lower_body_intermediate)
            else:
                return random.choice(lower_body_intermediate + lower_body_advanced)
        
        elif day_of_week == 1:  # Tuesday - HIIT
            if phase == "foundation":
                return random.choice(hiit_beginner)
            elif phase == "beginner":
                return random.choice(hiit_beginner + hiit_intermediate[:1])
            elif phase == "intermediate":
                return random.choice(hiit_intermediate)
            else:
                return random.choice(hiit_intermediate + hiit_advanced)
        
        elif day_of_week == 2:  # Wednesday - Upper Body
            if phase == "foundation":
                return random.choice(upper_body_beginner)
            elif phase == "beginner":
                return random.choice(upper_body_beginner + upper_body_intermediate[:1])
            elif phase == "intermediate":
                return random.choice(upper_body_intermediate)
            else:
                return random.choice(upper_body_intermediate + upper_body_advanced)
        
        elif day_of_week == 3:  # Thursday - Yoga/Recovery
            if week_num % 4 == 0:  # Every 4th week: recovery focus
                return random.choice(recovery_workouts)
            elif week_num % 2 == 0:
                return random.choice(yoga_workouts)
            else:
                return random.choice(pilates_workouts)
        
        elif day_of_week == 4:  # Friday - Full Body
            if phase == "foundation":
                return random.choice(full_body_beginner)
            elif phase == "beginner":
                return random.choice(full_body_beginner + full_body_intermediate[:1])
            elif phase == "intermediate":
                return random.choice(full_body_intermediate)
            else:
                return random.choice(full_body_intermediate + full_body_advanced)
        
        elif day_of_week == 5:  # Saturday - Cardio/Fun
            if week_num % 3 == 0:  # Every 3rd week: just stretching/recovery
                return random.choice(recovery_workouts)
            else:
                return random.choice(cardio_workouts)
        
        # Add occasional core work as secondary workout (1 in 3 non-rest days)
        return None
    
    # Generate 365 days of workouts
    start_date = today
    day_count = 0
    
    for i in range(365):
        workout_date = start_date + timedelta(days=i)
        date_str = workout_date.strftime("%Y-%m-%d")
        day_of_week = workout_date.weekday()
        week_num = i // 7 + 1
        
        # Get main workout for the day
        workout = get_workout_for_day(day_of_week, week_num, day_count)
        
        if workout:
            workout_copy = workout.copy()
            workout_copy['completed'] = False
            
            # Mark past workouts as completed (for demo)
            if workout_date < today:
                workout_copy['completed'] = True
            
            add_workout_to_calendar(date_str, workout_copy)
            
            # Add core workout on Monday/Friday (intermediate+)
            phase = get_phase(week_num)
            if phase in ["intermediate", "advanced", "peak"] and day_of_week in [0, 4]:
                if week_num % 2 == 0:  # Every other week
                    if phase == "intermediate":
                        core = random.choice(core_beginner + core_intermediate)
                    else:
                        core = random.choice(core_intermediate + core_advanced)
                    core_copy = core.copy()
                    core_copy['completed'] = False
                    if workout_date < today:
                        core_copy['completed'] = True
                    add_workout_to_calendar(date_str, core_copy)
        
        day_count += 1
    
    return True

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
# STREAK SYSTEM
# ============================================

def calculate_streak():
    """Calculate current workout streak based on consecutive completed days"""
    from datetime import datetime, timedelta
    
    calendar = load_calendar()
    if not calendar:
        return 0
    
    today = datetime.now().date()
    streak = 0
    check_date = today
    
    # Check today first
    today_str = today.strftime("%Y-%m-%d")
    today_workouts = calendar.get(today_str, [])
    today_completed = any(w.get('completed', False) for w in today_workouts) if today_workouts else False
    
    # If today not completed, start checking from yesterday
    if not today_completed:
        check_date = today - timedelta(days=1)
    
    # Count consecutive completed days
    while True:
        date_str = check_date.strftime("%Y-%m-%d")
        workouts = calendar.get(date_str, [])
        
        if not workouts:
            break
            
        # Check if all workouts for this day are completed
        all_completed = all(w.get('completed', False) for w in workouts)
        if all_completed and workouts:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    return streak

def get_streak_data():
    """Get comprehensive streak information"""
    from datetime import datetime, timedelta
    
    calendar = load_calendar()
    current_streak = calculate_streak()
    
    # Calculate best streak
    if not calendar:
        return {
            'current_streak': 0,
            'best_streak': 0,
            'total_completed': 0,
            'last_completed': None,
            'streak_status': 'none'
        }
    
    # Get all dates and sort them
    all_dates = sorted(calendar.keys())
    
    # Count total completed workouts
    total_completed = sum(
        1 for date_str in calendar 
        for w in calendar[date_str] 
        if w.get('completed', False)
    )
    
    # Find last completed date
    last_completed = None
    for date_str in reversed(all_dates):
        if any(w.get('completed', False) for w in calendar[date_str]):
            last_completed = date_str
            break
    
    # Calculate best streak
    best_streak = 0
    temp_streak = 0
    
    for i, date_str in enumerate(all_dates):
        workouts = calendar[date_str]
        all_completed = all(w.get('completed', False) for w in workouts) if workouts else False
        
        if all_completed and workouts:
            temp_streak += 1
            best_streak = max(best_streak, temp_streak)
        else:
            temp_streak = 0
    
    # Determine streak status
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    
    today_workouts = calendar.get(today_str, [])
    today_completed = any(w.get('completed', False) for w in today_workouts) if today_workouts else False
    
    if today_completed:
        streak_status = 'completed_today'
    elif today_workouts:
        streak_status = 'pending_today'
    elif current_streak > 0:
        streak_status = 'at_risk'
    else:
        streak_status = 'none'
    
    return {
        'current_streak': current_streak,
        'best_streak': max(best_streak, current_streak),
        'total_completed': total_completed,
        'last_completed': last_completed,
        'streak_status': streak_status
    }

def confirm_workout_completed(date_str):
    """Mark all workouts for a date as completed"""
    calendar = load_calendar()
    
    if date_str not in calendar:
        return False
    
    workouts = calendar[date_str]
    for i, workout in enumerate(workouts):
        mark_workout_complete(date_str, i, completed=True)
    
    return True

def get_completion_calendar():
    """Get calendar data formatted for streak visualization"""
    from datetime import datetime, timedelta
    
    calendar = load_calendar()
    today = datetime.now().date()
    
    # Get dates for the current month
    first_day = today.replace(day=1)
    
    # Calculate last day of month
    if today.month == 12:
        last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    completion_data = {}
    current_date = first_day
    
    while current_date <= last_day:
        date_str = current_date.strftime("%Y-%m-%d")
        workouts = calendar.get(date_str, [])
        
        if not workouts:
            status = 'no_workout'
        elif all(w.get('completed', False) for w in workouts):
            status = 'completed'
        elif current_date < today:
            status = 'missed'
        else:
            status = 'scheduled'
        
        completion_data[date_str] = {
            'status': status,
            'workouts': workouts,
            'date': current_date
        }
        
        current_date += timedelta(days=1)
    
    return completion_data

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
    },
    
    # ============================================
    # ONE YEAR TRANSFORMATION PROGRAM (52 WEEKS)
    # ============================================
    "one_year_transformation": {
        "name": "🗓️ 52-Week Total Body Transformation",
        "description": "A complete year-long fitness journey with progressive phases: Foundation → Build → Sculpt → Peak Performance. Transform your body and mindset!",
        "duration": "52 weeks (1 year)",
        "level": "All Levels (Progressive)",
        "goal": "Complete Body Transformation",
        "days_per_week": 5,
        "phases": {
            "Phase 1: Foundation (Weeks 1-13)": {
                "focus": "Build strength foundation, learn proper form, establish habits",
                "intensity": "Low to Moderate",
                "weeks": {
                    "Weeks 1-4: Beginner Foundation": {
                        "Day 1 - Lower Body": [
                            {"name": "Bodyweight Squats", "sets": 3, "reps": "12", "rest": "45s"},
                            {"name": "Glute Bridges", "sets": 3, "reps": "15", "rest": "45s"},
                            {"name": "Lunges", "sets": 2, "reps": "10 each", "rest": "45s"},
                            {"name": "Calf Raises", "sets": 3, "reps": "15", "rest": "30s"}
                        ],
                        "Day 2 - Upper Body": [
                            {"name": "Wall Push-ups", "sets": 3, "reps": "12", "rest": "45s"},
                            {"name": "Arm Circles", "sets": 2, "reps": "30s each", "rest": "30s"},
                            {"name": "Tricep Dips (chair)", "sets": 2, "reps": "10", "rest": "45s"},
                            {"name": "Superman Hold", "sets": 3, "reps": "15s", "rest": "30s"}
                        ],
                        "Day 3 - Core & Cardio": [
                            {"name": "Plank Hold", "sets": 3, "reps": "20s", "rest": "30s"},
                            {"name": "Dead Bug", "sets": 3, "reps": "10 each", "rest": "30s"},
                            {"name": "Jumping Jacks", "sets": 3, "reps": "30s", "rest": "30s"},
                            {"name": "March in Place", "sets": 3, "reps": "1 min", "rest": "30s"}
                        ],
                        "Day 4 - Active Recovery": [
                            {"name": "Yoga Flow", "sets": 1, "reps": "15 min", "rest": ""},
                            {"name": "Foam Rolling", "sets": 1, "reps": "10 min", "rest": ""},
                            {"name": "Light Walking", "sets": 1, "reps": "20 min", "rest": ""}
                        ],
                        "Day 5 - Full Body": [
                            {"name": "Squat to Calf Raise", "sets": 3, "reps": "12", "rest": "45s"},
                            {"name": "Incline Push-ups", "sets": 3, "reps": "10", "rest": "45s"},
                            {"name": "Bird Dogs", "sets": 3, "reps": "10 each", "rest": "30s"},
                            {"name": "Side Plank", "sets": 2, "reps": "15s each", "rest": "30s"}
                        ]
                    },
                    "Weeks 5-8: Building Endurance": {
                        "Day 1 - Lower Power": [
                            {"name": "Squats", "sets": 4, "reps": "15", "rest": "45s"},
                            {"name": "Sumo Squats", "sets": 3, "reps": "15", "rest": "45s"},
                            {"name": "Walking Lunges", "sets": 3, "reps": "12 each", "rest": "45s"},
                            {"name": "Glute Bridges", "sets": 4, "reps": "20", "rest": "30s"}
                        ],
                        "Day 2 - Upper Strength": [
                            {"name": "Push-ups (knees)", "sets": 3, "reps": "12", "rest": "45s"},
                            {"name": "Tricep Dips", "sets": 3, "reps": "12", "rest": "45s"},
                            {"name": "Plank Shoulder Taps", "sets": 3, "reps": "10 each", "rest": "30s"},
                            {"name": "Superman", "sets": 3, "reps": "12", "rest": "30s"}
                        ],
                        "Day 3 - HIIT Intro": [
                            {"name": "Jumping Jacks", "sets": 4, "reps": "30s", "rest": "15s"},
                            {"name": "High Knees", "sets": 4, "reps": "20s", "rest": "15s"},
                            {"name": "Mountain Climbers", "sets": 3, "reps": "20s", "rest": "20s"},
                            {"name": "Burpees (modified)", "sets": 3, "reps": "8", "rest": "30s"}
                        ],
                        "Day 4 - Flexibility": [
                            {"name": "Dynamic Stretching", "sets": 1, "reps": "10 min", "rest": ""},
                            {"name": "Yoga Flow", "sets": 1, "reps": "20 min", "rest": ""},
                            {"name": "Meditation", "sets": 1, "reps": "5 min", "rest": ""}
                        ],
                        "Day 5 - Full Body Circuit": [
                            {"name": "Squats", "sets": 3, "reps": "15", "rest": "30s"},
                            {"name": "Push-ups", "sets": 3, "reps": "10", "rest": "30s"},
                            {"name": "Plank", "sets": 3, "reps": "30s", "rest": "30s"},
                            {"name": "Lunges", "sets": 3, "reps": "12 each", "rest": "30s"}
                        ]
                    },
                    "Weeks 9-13: Foundation Complete": {
                        "Day 1 - Leg Day": [
                            {"name": "Squats", "sets": 4, "reps": "15", "rest": "45s"},
                            {"name": "Bulgarian Split Squats", "sets": 3, "reps": "10 each", "rest": "45s"},
                            {"name": "Hip Thrusts", "sets": 4, "reps": "15", "rest": "45s"},
                            {"name": "Calf Raises", "sets": 4, "reps": "20", "rest": "30s"}
                        ],
                        "Day 2 - Push Day": [
                            {"name": "Push-ups", "sets": 4, "reps": "12", "rest": "45s"},
                            {"name": "Pike Push-ups", "sets": 3, "reps": "8", "rest": "45s"},
                            {"name": "Diamond Push-ups", "sets": 3, "reps": "8", "rest": "45s"},
                            {"name": "Plank to Push-up", "sets": 3, "reps": "10", "rest": "30s"}
                        ],
                        "Day 3 - HIIT": [
                            {"name": "Burpees", "sets": 4, "reps": "10", "rest": "30s"},
                            {"name": "Jump Squats", "sets": 4, "reps": "12", "rest": "30s"},
                            {"name": "Mountain Climbers", "sets": 4, "reps": "30s", "rest": "20s"},
                            {"name": "High Knees", "sets": 4, "reps": "30s", "rest": "20s"}
                        ],
                        "Day 4 - Active Recovery": [
                            {"name": "Light Cardio", "sets": 1, "reps": "30 min", "rest": ""},
                            {"name": "Stretching", "sets": 1, "reps": "15 min", "rest": ""}
                        ],
                        "Day 5 - Full Body": [
                            {"name": "Squat Jumps", "sets": 3, "reps": "10", "rest": "45s"},
                            {"name": "Push-ups", "sets": 3, "reps": "12", "rest": "45s"},
                            {"name": "Plank", "sets": 3, "reps": "45s", "rest": "30s"},
                            {"name": "Glute Bridges", "sets": 3, "reps": "20", "rest": "30s"}
                        ]
                    }
                }
            },
            "Phase 2: Build (Weeks 14-26)": {
                "focus": "Increase intensity, build muscle, improve cardio endurance",
                "intensity": "Moderate to High",
                "weeks": {
                    "Weeks 14-18: Strength Building": {
                        "Day 1 - Lower Body Strength": [
                            {"name": "Squats", "sets": 4, "reps": "12", "rest": "60s"},
                            {"name": "Romanian Deadlifts", "sets": 4, "reps": "12", "rest": "60s"},
                            {"name": "Walking Lunges", "sets": 3, "reps": "15 each", "rest": "45s"},
                            {"name": "Hip Thrusts", "sets": 4, "reps": "15", "rest": "45s"},
                            {"name": "Calf Raises", "sets": 4, "reps": "20", "rest": "30s"}
                        ],
                        "Day 2 - Upper Body Strength": [
                            {"name": "Push-ups", "sets": 4, "reps": "15", "rest": "45s"},
                            {"name": "Pike Push-ups", "sets": 4, "reps": "10", "rest": "45s"},
                            {"name": "Tricep Dips", "sets": 4, "reps": "12", "rest": "45s"},
                            {"name": "Plank Rows", "sets": 3, "reps": "10 each", "rest": "45s"},
                            {"name": "Superman", "sets": 3, "reps": "15", "rest": "30s"}
                        ],
                        "Day 3 - HIIT": [
                            {"name": "Tabata Burpees", "sets": 8, "reps": "20s/10s", "rest": "1 min"},
                            {"name": "Tabata Squats", "sets": 8, "reps": "20s/10s", "rest": "1 min"},
                            {"name": "Tabata Mountain Climbers", "sets": 8, "reps": "20s/10s", "rest": ""}
                        ],
                        "Day 4 - Core Focus": [
                            {"name": "Plank", "sets": 4, "reps": "45s", "rest": "30s"},
                            {"name": "Bicycle Crunches", "sets": 4, "reps": "20", "rest": "30s"},
                            {"name": "Russian Twists", "sets": 4, "reps": "20", "rest": "30s"},
                            {"name": "Leg Raises", "sets": 3, "reps": "15", "rest": "30s"},
                            {"name": "Dead Bug", "sets": 3, "reps": "12 each", "rest": "30s"}
                        ],
                        "Day 5 - Full Body Power": [
                            {"name": "Jump Squats", "sets": 4, "reps": "12", "rest": "45s"},
                            {"name": "Explosive Push-ups", "sets": 3, "reps": "10", "rest": "45s"},
                            {"name": "Box Jumps", "sets": 3, "reps": "10", "rest": "45s"},
                            {"name": "Burpees", "sets": 3, "reps": "10", "rest": "45s"}
                        ]
                    },
                    "Weeks 19-22: Progressive Overload": {
                        "Day 1 - Legs & Glutes": [
                            {"name": "Squats", "sets": 5, "reps": "12", "rest": "60s"},
                            {"name": "Single Leg RDL", "sets": 4, "reps": "10 each", "rest": "45s"},
                            {"name": "Bulgarian Split Squats", "sets": 4, "reps": "10 each", "rest": "45s"},
                            {"name": "Hip Thrusts", "sets": 5, "reps": "15", "rest": "45s"},
                            {"name": "Wall Sit", "sets": 3, "reps": "45s", "rest": "30s"}
                        ],
                        "Day 2 - Push & Core": [
                            {"name": "Decline Push-ups", "sets": 4, "reps": "12", "rest": "45s"},
                            {"name": "Diamond Push-ups", "sets": 4, "reps": "10", "rest": "45s"},
                            {"name": "Pike Push-ups", "sets": 4, "reps": "10", "rest": "45s"},
                            {"name": "Plank", "sets": 3, "reps": "60s", "rest": "30s"},
                            {"name": "V-Ups", "sets": 3, "reps": "12", "rest": "30s"}
                        ],
                        "Day 3 - Cardio Blast": [
                            {"name": "AMRAP 20 min Circuit", "sets": 1, "reps": "See below", "rest": ""},
                            {"name": "→ 10 Burpees", "sets": 0, "reps": "", "rest": ""},
                            {"name": "→ 15 Jump Squats", "sets": 0, "reps": "", "rest": ""},
                            {"name": "→ 20 Mountain Climbers", "sets": 0, "reps": "", "rest": ""},
                            {"name": "→ 10 Push-ups", "sets": 0, "reps": "", "rest": ""}
                        ],
                        "Day 4 - Active Recovery": [
                            {"name": "Yoga", "sets": 1, "reps": "30 min", "rest": ""},
                            {"name": "Light Walk", "sets": 1, "reps": "20 min", "rest": ""}
                        ],
                        "Day 5 - Total Body": [
                            {"name": "Squat to Press", "sets": 4, "reps": "12", "rest": "45s"},
                            {"name": "Renegade Rows", "sets": 4, "reps": "10 each", "rest": "45s"},
                            {"name": "Glute Bridge March", "sets": 4, "reps": "12 each", "rest": "45s"},
                            {"name": "Plank to Push-up", "sets": 3, "reps": "10", "rest": "30s"}
                        ]
                    },
                    "Weeks 23-26: Build Peak": {
                        "Day 1 - Lower Intensity": [
                            {"name": "Pistol Squat Progression", "sets": 4, "reps": "8 each", "rest": "60s"},
                            {"name": "Romanian Deadlift", "sets": 5, "reps": "12", "rest": "60s"},
                            {"name": "Pulse Squats", "sets": 4, "reps": "20", "rest": "45s"},
                            {"name": "Donkey Kicks", "sets": 4, "reps": "15 each", "rest": "30s"}
                        ],
                        "Day 2 - Upper Intensity": [
                            {"name": "Clapping Push-ups", "sets": 4, "reps": "8", "rest": "60s"},
                            {"name": "Handstand Hold (wall)", "sets": 4, "reps": "20s", "rest": "60s"},
                            {"name": "Tricep Push-ups", "sets": 4, "reps": "12", "rest": "45s"},
                            {"name": "Plank Shoulder Taps", "sets": 4, "reps": "15 each", "rest": "30s"}
                        ],
                        "Day 3 - EMOM 30": [
                            {"name": "Min 1: 15 Squats", "sets": 10, "reps": "rounds", "rest": ""},
                            {"name": "Min 2: 10 Push-ups", "sets": 10, "reps": "rounds", "rest": ""},
                            {"name": "Min 3: 20 Mountain Climbers", "sets": 10, "reps": "rounds", "rest": ""}
                        ],
                        "Day 4 - Mobility": [
                            {"name": "Deep Stretching", "sets": 1, "reps": "30 min", "rest": ""},
                            {"name": "Foam Rolling", "sets": 1, "reps": "15 min", "rest": ""}
                        ],
                        "Day 5 - Circuit Training": [
                            {"name": "4 Rounds", "sets": 4, "reps": "circuit", "rest": "90s"},
                            {"name": "→ 12 Jump Lunges", "sets": 0, "reps": "", "rest": ""},
                            {"name": "→ 10 Pike Push-ups", "sets": 0, "reps": "", "rest": ""},
                            {"name": "→ 15 Hip Thrusts", "sets": 0, "reps": "", "rest": ""},
                            {"name": "→ 45s Plank", "sets": 0, "reps": "", "rest": ""}
                        ]
                    }
                }
            },
            "Phase 3: Sculpt (Weeks 27-39)": {
                "focus": "Define muscles, increase definition, maintain strength",
                "intensity": "High",
                "weeks": {
                    "Weeks 27-31: Definition": {
                        "Day 1 - Glute Sculpt": [
                            {"name": "Hip Thrusts", "sets": 5, "reps": "15", "rest": "45s"},
                            {"name": "Sumo Squats", "sets": 4, "reps": "15", "rest": "45s"},
                            {"name": "Cable Kickbacks (band)", "sets": 4, "reps": "15 each", "rest": "30s"},
                            {"name": "Fire Hydrants", "sets": 4, "reps": "15 each", "rest": "30s"},
                            {"name": "Frog Pumps", "sets": 3, "reps": "30", "rest": "30s"}
                        ],
                        "Day 2 - Arms & Shoulders": [
                            {"name": "Pike Push-ups", "sets": 5, "reps": "10", "rest": "45s"},
                            {"name": "Diamond Push-ups", "sets": 4, "reps": "12", "rest": "45s"},
                            {"name": "Tricep Dips", "sets": 4, "reps": "15", "rest": "45s"},
                            {"name": "Plank Up-Downs", "sets": 4, "reps": "12", "rest": "30s"}
                        ],
                        "Day 3 - HIIT Burn": [
                            {"name": "Tabata Rounds x 6", "sets": 6, "reps": "4 min each", "rest": "1 min"},
                            {"name": "→ Burpees, Squats, Mt. Climbers, Push-ups, Lunges, Plank", "sets": 0, "reps": "", "rest": ""}
                        ],
                        "Day 4 - Core Chisel": [
                            {"name": "Hollow Body Hold", "sets": 4, "reps": "30s", "rest": "30s"},
                            {"name": "V-Ups", "sets": 4, "reps": "15", "rest": "30s"},
                            {"name": "Russian Twists", "sets": 4, "reps": "20", "rest": "30s"},
                            {"name": "Plank", "sets": 3, "reps": "60s", "rest": "30s"},
                            {"name": "Leg Raises", "sets": 3, "reps": "15", "rest": "30s"}
                        ],
                        "Day 5 - Full Body Sculpt": [
                            {"name": "Tempo Squats (3s down)", "sets": 4, "reps": "12", "rest": "45s"},
                            {"name": "Slow Push-ups (3s down)", "sets": 4, "reps": "10", "rest": "45s"},
                            {"name": "Slow Glute Bridge", "sets": 4, "reps": "15", "rest": "45s"},
                            {"name": "Isometric Holds", "sets": 3, "reps": "30s each", "rest": "30s"}
                        ]
                    },
                    "Weeks 32-35: Refinement": {
                        "Day 1 - Lower Shred": [
                            {"name": "Jump Squats", "sets": 4, "reps": "15", "rest": "30s"},
                            {"name": "Walking Lunges", "sets": 4, "reps": "20 each", "rest": "45s"},
                            {"name": "Step-ups", "sets": 4, "reps": "12 each", "rest": "45s"},
                            {"name": "Squat Pulses", "sets": 3, "reps": "30", "rest": "30s"}
                        ],
                        "Day 2 - Upper Shred": [
                            {"name": "Push-up Variations (10 each)", "sets": 4, "reps": "mix", "rest": "45s"},
                            {"name": "Tricep Burnout", "sets": 3, "reps": "to failure", "rest": "60s"},
                            {"name": "Plank Complex", "sets": 3, "reps": "60s", "rest": "45s"}
                        ],
                        "Day 3 - Cardio Intervals": [
                            {"name": "30-20-10 x 5 rounds", "sets": 5, "reps": "sprint format", "rest": "90s"},
                            {"name": "→ 30s easy, 20s moderate, 10s max", "sets": 0, "reps": "", "rest": ""}
                        ],
                        "Day 4 - Active Recovery": [
                            {"name": "Yoga Flow", "sets": 1, "reps": "45 min", "rest": ""}
                        ],
                        "Day 5 - MetCon": [
                            {"name": "AMRAP 25 min", "sets": 1, "reps": "see below", "rest": ""},
                            {"name": "→ 5 Burpees, 10 Push-ups, 15 Squats, 20 Lunges", "sets": 0, "reps": "", "rest": ""}
                        ]
                    },
                    "Weeks 36-39: Peak Definition": {
                        "Day 1 - Legs Advanced": [
                            {"name": "Pistol Squats", "sets": 4, "reps": "6 each", "rest": "60s"},
                            {"name": "Nordic Curl Negatives", "sets": 3, "reps": "6", "rest": "60s"},
                            {"name": "Single Leg Hip Thrust", "sets": 4, "reps": "12 each", "rest": "45s"},
                            {"name": "Sissy Squats", "sets": 3, "reps": "12", "rest": "45s"}
                        ],
                        "Day 2 - Upper Advanced": [
                            {"name": "Archer Push-ups", "sets": 4, "reps": "6 each", "rest": "60s"},
                            {"name": "Pseudo Planche Push-ups", "sets": 3, "reps": "8", "rest": "60s"},
                            {"name": "L-Sit Hold", "sets": 4, "reps": "15s", "rest": "45s"}
                        ],
                        "Day 3 - HIIT Max": [
                            {"name": "Death by Burpees", "sets": 1, "reps": "EMOM until fail", "rest": ""},
                            {"name": "→ Start with 1, add 1 each minute", "sets": 0, "reps": "", "rest": ""}
                        ],
                        "Day 4 - Recovery": [
                            {"name": "Mobility Work", "sets": 1, "reps": "30 min", "rest": ""}
                        ],
                        "Day 5 - Test Day": [
                            {"name": "Max Push-ups in 2 min", "sets": 1, "reps": "test", "rest": "3 min"},
                            {"name": "Max Squats in 2 min", "sets": 1, "reps": "test", "rest": "3 min"},
                            {"name": "Max Plank Hold", "sets": 1, "reps": "test", "rest": ""}
                        ]
                    }
                }
            },
            "Phase 4: Peak Performance (Weeks 40-52)": {
                "focus": "Athletic performance, power, maintain year's progress",
                "intensity": "Variable (Periodization)",
                "weeks": {
                    "Weeks 40-44: Power Phase": {
                        "Day 1 - Explosive Lower": [
                            {"name": "Box Jumps", "sets": 5, "reps": "8", "rest": "60s"},
                            {"name": "Jump Lunges", "sets": 4, "reps": "10 each", "rest": "45s"},
                            {"name": "Broad Jumps", "sets": 4, "reps": "6", "rest": "60s"},
                            {"name": "Squat Jumps", "sets": 4, "reps": "12", "rest": "45s"}
                        ],
                        "Day 2 - Explosive Upper": [
                            {"name": "Clapping Push-ups", "sets": 5, "reps": "8", "rest": "60s"},
                            {"name": "Plyo Push-ups", "sets": 4, "reps": "8", "rest": "60s"},
                            {"name": "Medicine Ball Throws", "sets": 4, "reps": "10", "rest": "45s"}
                        ],
                        "Day 3 - Sprint HIIT": [
                            {"name": "Sprint Intervals", "sets": 10, "reps": "30s sprint/30s rest", "rest": ""},
                            {"name": "Cool Down Jog", "sets": 1, "reps": "10 min", "rest": ""}
                        ],
                        "Day 4 - Strength Maintenance": [
                            {"name": "Full Body Circuit", "sets": 4, "reps": "10 each move", "rest": "60s"},
                            {"name": "→ Squats, Push-ups, Lunges, Plank", "sets": 0, "reps": "", "rest": ""}
                        ],
                        "Day 5 - Sport-Specific": [
                            {"name": "Agility Ladder", "sets": 4, "reps": "30s", "rest": "30s"},
                            {"name": "Cone Drills", "sets": 4, "reps": "30s", "rest": "30s"},
                            {"name": "Plyometric Circuit", "sets": 3, "reps": "full", "rest": "60s"}
                        ]
                    },
                    "Weeks 45-48: Performance Testing": {
                        "Day 1 - Strength Test": [
                            {"name": "Max Push-ups (1 set)", "sets": 1, "reps": "max", "rest": ""},
                            {"name": "Max Squats (1 set)", "sets": 1, "reps": "max", "rest": ""},
                            {"name": "Max Plank Hold", "sets": 1, "reps": "max time", "rest": ""}
                        ],
                        "Day 2 - Endurance": [
                            {"name": "1000m Run for Time", "sets": 1, "reps": "test", "rest": ""},
                            {"name": "100 Burpees for Time", "sets": 1, "reps": "test", "rest": ""}
                        ],
                        "Day 3 - Power Test": [
                            {"name": "Standing Long Jump", "sets": 3, "reps": "test", "rest": ""},
                            {"name": "Vertical Jump", "sets": 3, "reps": "test", "rest": ""}
                        ],
                        "Day 4 - Recovery": [
                            {"name": "Yoga & Stretching", "sets": 1, "reps": "45 min", "rest": ""}
                        ],
                        "Day 5 - Mixed Training": [
                            {"name": "CrossFit Style WOD", "sets": 1, "reps": "20 min", "rest": ""}
                        ]
                    },
                    "Weeks 49-52: Celebration & Maintenance": {
                        "Day 1 - Favorite Workout": [
                            {"name": "Choose Your Best Workout from the Year", "sets": 1, "reps": "full", "rest": ""}
                        ],
                        "Day 2 - Fun Fitness": [
                            {"name": "Dance Workout", "sets": 1, "reps": "30 min", "rest": ""},
                            {"name": "Or Sport of Choice", "sets": 1, "reps": "30 min", "rest": ""}
                        ],
                        "Day 3 - Challenge Day": [
                            {"name": "Final Test: All PRs", "sets": 1, "reps": "test all", "rest": ""}
                        ],
                        "Day 4 - Reflection": [
                            {"name": "Light Movement & Journaling", "sets": 1, "reps": "30 min", "rest": ""}
                        ],
                        "Day 5 - Celebration Workout": [
                            {"name": "Year End Special Circuit", "sets": 4, "reps": "full", "rest": "60s"},
                            {"name": "You Made It! 🎉", "sets": 1, "reps": "celebrate!", "rest": ""}
                        ]
                    }
                }
            }
        },
        "milestone_rewards": {
            "Week 4": "🌟 Foundation Started Badge",
            "Week 13": "💪 Phase 1 Complete - Foundation Strong",
            "Week 26": "🔥 Half Year Hero - Halfway There!",
            "Week 39": "⭐ Sculpted Success - 3 Quarters Done",
            "Week 52": "👑 TRANSFORMATION COMPLETE - You're a Champion!"
        }
    }
}

def get_workout_programs():
    """Return all available workout programs"""
    return GIRLS_WORKOUT_PROGRAMS

def get_program_by_id(program_id):
    """Get a specific program by its ID"""
    return GIRLS_WORKOUT_PROGRAMS.get(program_id)