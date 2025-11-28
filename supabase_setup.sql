-- ============================================
-- JADE FITNESS HUB - SUPABASE DATABASE SETUP
-- ============================================
-- Run this SQL in your Supabase SQL Editor:
-- https://supabase.com/dashboard/project/pezmmnfgelrcodwgxpdl/sql

-- 1. Create the workouts table (for saved YouTube videos)
CREATE TABLE IF NOT EXISTS workouts (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    channel TEXT,
    url TEXT NOT NULL,
    thumbnail TEXT,
    category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create the workout_calendar table (for scheduled workouts)
CREATE TABLE IF NOT EXISTS workout_calendar (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    name TEXT NOT NULL,
    type TEXT,
    duration TEXT,
    notes TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_workouts_category ON workouts(category);
CREATE INDEX IF NOT EXISTS idx_workouts_created_at ON workouts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_calendar_date ON workout_calendar(date);
CREATE INDEX IF NOT EXISTS idx_calendar_completed ON workout_calendar(completed);

-- 4. Enable Row Level Security (RLS) - Optional but recommended
-- Uncomment these if you want to add user authentication later

-- ALTER TABLE workouts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE workout_calendar ENABLE ROW LEVEL SECURITY;

-- Allow public access (for now, since we're not using auth)
-- CREATE POLICY "Allow public access to workouts" ON workouts FOR ALL USING (true);
-- CREATE POLICY "Allow public access to calendar" ON workout_calendar FOR ALL USING (true);

-- 5. Grant permissions
GRANT ALL ON workouts TO anon;
GRANT ALL ON workout_calendar TO anon;
GRANT USAGE, SELECT ON SEQUENCE workouts_id_seq TO anon;
GRANT USAGE, SELECT ON SEQUENCE workout_calendar_id_seq TO anon;

-- ============================================
-- DONE! Your tables are ready to use.
-- ============================================
