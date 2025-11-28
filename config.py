# Supabase Configuration
# Get these from: https://supabase.com/dashboard/project/pezmmnfgelrcodwgxpdl/settings/api

import os

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Supabase credentials - use environment variables or defaults
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://pezmmnfgelrcodwgxpdl.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Table names
WORKOUTS_TABLE = "workouts"
CALENDAR_TABLE = "workout_calendar"
