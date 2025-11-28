# ============================================
# EXERCISE LIBRARY WITH FREE GIF DEMONSTRATIONS
# Sources: Wger API, ExerciseDB (via public endpoints)
# ============================================

# Exercise database with GIF demonstrations from free sources
# GIFs are from public exercise databases and fitness resources

EXERCISE_LIBRARY = {
    # ===== LOWER BODY =====
    "squats": {
        "name": "Squats",
        "category": "Lower Body",
        "muscle_groups": ["Quadriceps", "Glutes", "Hamstrings", "Core"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/SQUAT.gif",
        "video_url": "https://www.youtube.com/watch?v=aclHkVaku9U",
        "instructions": {
            "setup": "Stand with feet shoulder-width apart, toes slightly pointed out. Arms can be extended forward or hands clasped at chest.",
            "execution": [
                "Push your hips back as if sitting into a chair",
                "Bend your knees and lower down until thighs are parallel to floor",
                "Keep your chest up and back straight",
                "Press through your heels to stand back up",
                "Squeeze your glutes at the top"
            ],
            "breathing": "Inhale as you lower down, exhale as you push up",
            "common_mistakes": [
                "Knees caving inward - Keep knees tracking over toes",
                "Leaning too far forward - Keep chest up, engage core",
                "Not going deep enough - Aim for thighs parallel to floor",
                "Rising on toes - Keep weight in heels"
            ],
            "tips": "Imagine you're sitting back into a chair. Keep your core tight throughout the movement."
        },
        "reps_range": "12-15",
        "sets_range": "3-4"
    },
    
    "lunges": {
        "name": "Lunges",
        "category": "Lower Body",
        "muscle_groups": ["Quadriceps", "Glutes", "Hamstrings"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lunges.gif",
        "video_url": "https://www.youtube.com/watch?v=QOVaHwm-Q6U",
        "instructions": {
            "setup": "Stand tall with feet hip-width apart, hands on hips or at sides.",
            "execution": [
                "Take a big step forward with your right leg",
                "Lower your body until both knees are at 90 degrees",
                "Keep your front knee over your ankle, not past your toes",
                "Push through your front heel to return to start",
                "Repeat on the other side"
            ],
            "breathing": "Inhale as you step and lower, exhale as you push back up",
            "common_mistakes": [
                "Front knee going past toes - Take a bigger step",
                "Torso leaning forward - Keep chest up and proud",
                "Back knee hitting the ground hard - Control the descent",
                "Narrow stance - Step out slightly for balance"
            ],
            "tips": "Focus on dropping straight down, not forward. Keep your core engaged for stability."
        },
        "reps_range": "10-12 each leg",
        "sets_range": "3"
    },
    
    "glute_bridges": {
        "name": "Glute Bridges",
        "category": "Lower Body",
        "muscle_groups": ["Glutes", "Hamstrings", "Core"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Glute-Bridge.gif",
        "video_url": "https://www.youtube.com/watch?v=OUgsJ8-Vi0E",
        "instructions": {
            "setup": "Lie on your back with knees bent, feet flat on floor hip-width apart. Arms at sides, palms down.",
            "execution": [
                "Press through your heels to lift your hips off the ground",
                "Squeeze your glutes at the top",
                "Create a straight line from shoulders to knees",
                "Hold for 1-2 seconds at the top",
                "Lower back down with control"
            ],
            "breathing": "Exhale as you lift, inhale as you lower",
            "common_mistakes": [
                "Overarching lower back - Focus on glute squeeze, not height",
                "Pushing through toes - Keep weight in heels",
                "Not squeezing at the top - Pause and squeeze glutes",
                "Rushing the movement - Control both up and down"
            ],
            "tips": "Really focus on squeezing your glutes at the top. You should feel this in your butt, not your lower back."
        },
        "reps_range": "15-20",
        "sets_range": "3"
    },
    
    "donkey_kicks": {
        "name": "Donkey Kicks",
        "category": "Lower Body",
        "muscle_groups": ["Glutes", "Hamstrings", "Core"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Donkey-Kicks.gif",
        "video_url": "https://www.youtube.com/watch?v=YrEB-h1YC-A",
        "instructions": {
            "setup": "Start on all fours with hands under shoulders and knees under hips.",
            "execution": [
                "Keep your right knee bent at 90 degrees",
                "Lift your right leg toward the ceiling",
                "Keep your foot flexed and squeeze your glute",
                "Lower back down with control",
                "Complete all reps before switching legs"
            ],
            "breathing": "Exhale as you kick up, inhale as you lower",
            "common_mistakes": [
                "Arching lower back - Keep core tight and back flat",
                "Swinging the leg - Use controlled movements",
                "Not squeezing at the top - Pause and contract glute",
                "Shifting weight to one side - Stay centered"
            ],
            "tips": "Imagine pressing your foot toward the ceiling. Keep your core engaged to protect your lower back."
        },
        "reps_range": "15-20 each leg",
        "sets_range": "3"
    },
    
    "fire_hydrants": {
        "name": "Fire Hydrants",
        "category": "Lower Body",
        "muscle_groups": ["Glutes", "Hip Abductors", "Core"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Fire-Hydrant.gif",
        "video_url": "https://www.youtube.com/watch?v=La3xYT8MGks",
        "instructions": {
            "setup": "Start on all fours with hands under shoulders and knees under hips.",
            "execution": [
                "Keep your knee bent at 90 degrees",
                "Lift your right leg out to the side",
                "Raise until your thigh is parallel to the floor",
                "Keep your hips square - don't rotate",
                "Lower with control and repeat"
            ],
            "breathing": "Exhale as you lift, inhale as you lower",
            "common_mistakes": [
                "Rotating hips - Keep hips square to the ground",
                "Lifting too high - Focus on controlled range",
                "Collapsing through shoulders - Keep arms strong",
                "Rushing - Slow and controlled wins"
            ],
            "tips": "This exercise is great for hip mobility and glute activation. Keep movements slow and controlled."
        },
        "reps_range": "15 each side",
        "sets_range": "3"
    },
    
    "sumo_squats": {
        "name": "Sumo Squats",
        "category": "Lower Body",
        "muscle_groups": ["Inner Thighs", "Glutes", "Quadriceps"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Sumo-Squat.gif",
        "video_url": "https://www.youtube.com/watch?v=9ZuXKqRbT9k",
        "instructions": {
            "setup": "Stand with feet wider than shoulder-width, toes pointed out at 45 degrees.",
            "execution": [
                "Push your hips back and bend your knees",
                "Lower down keeping your chest up",
                "Keep knees tracking over your toes",
                "Go as low as comfortable (thighs parallel or below)",
                "Press through heels to stand back up"
            ],
            "breathing": "Inhale down, exhale up",
            "common_mistakes": [
                "Knees caving in - Push knees out over toes",
                "Leaning forward - Keep chest proud",
                "Stance too narrow - Go wider for sumo position",
                "Not going deep enough - Work on hip mobility"
            ],
            "tips": "This variation targets your inner thighs more than regular squats. Keep your core tight."
        },
        "reps_range": "12-15",
        "sets_range": "3"
    },
    
    # ===== UPPER BODY =====
    "push_ups": {
        "name": "Push-Ups",
        "category": "Upper Body",
        "muscle_groups": ["Chest", "Triceps", "Shoulders", "Core"],
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif",
        "video_url": "https://www.youtube.com/watch?v=IODxDxX7oi4",
        "instructions": {
            "setup": "Start in a high plank position with hands slightly wider than shoulders. Body in a straight line from head to heels.",
            "execution": [
                "Keep your core tight and body straight",
                "Lower your chest toward the floor",
                "Keep elbows at 45-degree angle from body",
                "Lower until chest nearly touches the ground",
                "Push back up to starting position"
            ],
            "breathing": "Inhale as you lower, exhale as you push up",
            "common_mistakes": [
                "Hips sagging - Engage core, keep body straight",
                "Elbows flaring out - Keep them at 45 degrees",
                "Not going low enough - Chest should nearly touch floor",
                "Head dropping - Keep neck neutral, look slightly ahead"
            ],
            "tips": "If regular push-ups are too hard, start with knee push-ups or incline push-ups against a wall or bench."
        },
        "reps_range": "8-15",
        "sets_range": "3"
    },
    
    "tricep_dips": {
        "name": "Tricep Dips",
        "category": "Upper Body",
        "muscle_groups": ["Triceps", "Shoulders", "Chest"],
        "equipment": "Chair/Bench",
        "difficulty": "Intermediate",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Triceps-Dips-on-Floor.gif",
        "video_url": "https://www.youtube.com/watch?v=6kALZikXxLc",
        "instructions": {
            "setup": "Sit on edge of chair/bench with hands gripping the edge beside your hips. Walk feet out.",
            "execution": [
                "Slide your butt off the edge of the bench",
                "Lower your body by bending your elbows",
                "Go down until elbows are at 90 degrees",
                "Keep your back close to the bench",
                "Push through your palms to straighten arms"
            ],
            "breathing": "Inhale as you lower, exhale as you push up",
            "common_mistakes": [
                "Going too low - Stop at 90 degrees to protect shoulders",
                "Elbows flaring out - Keep them pointing back",
                "Shoulders shrugging up - Keep shoulders down and back",
                "Using legs too much - Let arms do the work"
            ],
            "tips": "Bend your knees to make it easier, or extend legs straight for more challenge."
        },
        "reps_range": "10-15",
        "sets_range": "3"
    },
    
    "plank_shoulder_taps": {
        "name": "Plank Shoulder Taps",
        "category": "Upper Body",
        "muscle_groups": ["Core", "Shoulders", "Chest", "Arms"],
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Plank-Shoulder-Tap.gif",
        "video_url": "https://www.youtube.com/watch?v=LEZq7QZ8ySQ",
        "instructions": {
            "setup": "Start in a high plank position with hands under shoulders, feet hip-width apart.",
            "execution": [
                "Keep your core tight and hips stable",
                "Lift your right hand and tap your left shoulder",
                "Place hand back down",
                "Lift left hand and tap right shoulder",
                "Minimize hip rotation throughout"
            ],
            "breathing": "Breathe steadily throughout - don't hold your breath",
            "common_mistakes": [
                "Hips rotating side to side - Widen feet for stability",
                "Butt raising up - Keep body in straight line",
                "Rushing - Go slow and controlled",
                "Forgetting to breathe - Keep breathing steady"
            ],
            "tips": "Widen your feet for more stability. The goal is to keep your hips completely still."
        },
        "reps_range": "20 total (10 each side)",
        "sets_range": "3"
    },
    
    # ===== CORE =====
    "plank": {
        "name": "Plank",
        "category": "Core",
        "muscle_groups": ["Core", "Shoulders", "Back", "Glutes"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Plank.gif",
        "video_url": "https://www.youtube.com/watch?v=pSHjTRCQxIw",
        "instructions": {
            "setup": "Start face down with forearms on the ground, elbows under shoulders.",
            "execution": [
                "Lift your body off the ground",
                "Create a straight line from head to heels",
                "Engage your core - pull belly button to spine",
                "Keep your glutes tight",
                "Hold the position for desired time"
            ],
            "breathing": "Breathe normally - don't hold your breath",
            "common_mistakes": [
                "Hips sagging - Squeeze glutes and engage core",
                "Butt too high - Lower hips to create straight line",
                "Looking up - Keep neck neutral, look at floor",
                "Holding breath - Keep breathing steadily"
            ],
            "tips": "Start with shorter holds (20-30 seconds) and build up. Quality over quantity!"
        },
        "reps_range": "30-60 seconds",
        "sets_range": "3"
    },
    
    "bicycle_crunches": {
        "name": "Bicycle Crunches",
        "category": "Core",
        "muscle_groups": ["Abs", "Obliques"],
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bicycle-Crunch.gif",
        "video_url": "https://www.youtube.com/watch?v=9FGilxCbdz8",
        "instructions": {
            "setup": "Lie on your back with hands behind your head, legs raised with knees at 90 degrees.",
            "execution": [
                "Lift your shoulders off the ground",
                "Rotate and bring right elbow toward left knee",
                "Simultaneously extend right leg out",
                "Switch sides in a pedaling motion",
                "Keep your lower back pressed into the floor"
            ],
            "breathing": "Exhale as you rotate to each side",
            "common_mistakes": [
                "Pulling on neck - Hands support head, don't pull",
                "Moving too fast - Slow and controlled is better",
                "Not fully extending leg - Straighten leg out fully",
                "Lower back arching - Keep it pressed to floor"
            ],
            "tips": "Focus on the rotation through your torso, not just touching elbow to knee."
        },
        "reps_range": "20 total (10 each side)",
        "sets_range": "3"
    },
    
    "mountain_climbers": {
        "name": "Mountain Climbers",
        "category": "Core",
        "muscle_groups": ["Core", "Shoulders", "Hip Flexors", "Cardio"],
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Mountain-Climber.gif",
        "video_url": "https://www.youtube.com/watch?v=nmwgirgXLYM",
        "instructions": {
            "setup": "Start in a high plank position with hands under shoulders.",
            "execution": [
                "Drive your right knee toward your chest",
                "Quickly switch legs, extending right leg back",
                "Drive left knee toward chest",
                "Continue alternating in a running motion",
                "Keep your hips down and core tight"
            ],
            "breathing": "Breathe rhythmically with the movement",
            "common_mistakes": [
                "Butt rising up - Keep hips level with shoulders",
                "Bouncing - Keep upper body stable",
                "Not bringing knees far enough - Drive knees to chest",
                "Looking up - Keep neck neutral"
            ],
            "tips": "Start slow to get the form right, then increase speed for more cardio challenge."
        },
        "reps_range": "30-40 total",
        "sets_range": "3"
    },
    
    "dead_bug": {
        "name": "Dead Bug",
        "category": "Core",
        "muscle_groups": ["Core", "Hip Flexors", "Lower Back"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dead-Bug.gif",
        "video_url": "https://www.youtube.com/watch?v=I5xbsA71v1A",
        "instructions": {
            "setup": "Lie on your back with arms extended toward ceiling and knees bent at 90 degrees over hips.",
            "execution": [
                "Press your lower back into the floor",
                "Slowly lower your right arm and left leg",
                "Keep your lower back pressed down",
                "Return to start and switch sides",
                "Move slowly and with control"
            ],
            "breathing": "Exhale as you lower limbs, inhale as you return",
            "common_mistakes": [
                "Lower back arching - Keep it pressed to floor",
                "Moving too fast - Go slow and controlled",
                "Holding breath - Keep breathing steadily",
                "Not extending fully - Reach arm and leg out fully"
            ],
            "tips": "If your back arches, don't lower limbs as far. Build up range gradually."
        },
        "reps_range": "10-12 each side",
        "sets_range": "3"
    },
    
    "russian_twists": {
        "name": "Russian Twists",
        "category": "Core",
        "muscle_groups": ["Obliques", "Abs", "Hip Flexors"],
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Russian-Twist.gif",
        "video_url": "https://www.youtube.com/watch?v=wkD8rjkodUI",
        "instructions": {
            "setup": "Sit with knees bent, feet flat or lifted. Lean back slightly, keeping back straight. Hands together at chest.",
            "execution": [
                "Engage your core and lean back slightly",
                "Rotate your torso to the right",
                "Touch the ground beside your hip",
                "Rotate to the left side",
                "Keep your core tight throughout"
            ],
            "breathing": "Exhale as you rotate to each side",
            "common_mistakes": [
                "Rounding the back - Keep chest up and back straight",
                "Moving just arms - Rotate from your core",
                "Feet moving around - Keep lower body stable",
                "Going too fast - Control the movement"
            ],
            "tips": "Lift your feet off the ground for more challenge. Add a weight for extra difficulty."
        },
        "reps_range": "20 total (10 each side)",
        "sets_range": "3"
    },
    
    # ===== CARDIO =====
    "jumping_jacks": {
        "name": "Jumping Jacks",
        "category": "Cardio",
        "muscle_groups": ["Full Body", "Cardio"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-Jacks.gif",
        "video_url": "https://www.youtube.com/watch?v=c4DAnQ6DtF8",
        "instructions": {
            "setup": "Stand with feet together and arms at your sides.",
            "execution": [
                "Jump and spread your feet wider than hip-width",
                "Simultaneously raise your arms overhead",
                "Jump back to starting position",
                "Arms return to sides as feet come together",
                "Repeat in a continuous rhythm"
            ],
            "breathing": "Breathe naturally with the rhythm",
            "common_mistakes": [
                "Landing hard - Land softly on balls of feet",
                "Arms not going full range - Reach overhead fully",
                "Not jumping wide enough - Get a good spread",
                "Holding breath - Keep breathing rhythmically"
            ],
            "tips": "Great warm-up exercise! Do low-impact version by stepping out instead of jumping."
        },
        "reps_range": "30-50",
        "sets_range": "3"
    },
    
    "burpees": {
        "name": "Burpees",
        "category": "Cardio",
        "muscle_groups": ["Full Body", "Cardio", "Chest", "Legs"],
        "equipment": "Bodyweight",
        "difficulty": "Advanced",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Burpee.gif",
        "video_url": "https://www.youtube.com/watch?v=dZgVxmf6jkA",
        "instructions": {
            "setup": "Stand with feet shoulder-width apart.",
            "execution": [
                "Squat down and place hands on the floor",
                "Jump or step your feet back into a plank",
                "Do a push-up (optional)",
                "Jump or step feet back to hands",
                "Explosively jump up with arms overhead"
            ],
            "breathing": "Exhale on the jump up",
            "common_mistakes": [
                "Skipping the push-up - Include it for full benefit",
                "Not jumping high enough - Give it full effort",
                "Sloppy plank - Keep body straight in plank",
                "Landing hard - Land softly with bent knees"
            ],
            "tips": "Modify by stepping instead of jumping, or skip the push-up when starting out."
        },
        "reps_range": "8-12",
        "sets_range": "3"
    },
    
    "high_knees": {
        "name": "High Knees",
        "category": "Cardio",
        "muscle_groups": ["Cardio", "Hip Flexors", "Core", "Legs"],
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/High-Knee-Run.gif",
        "video_url": "https://www.youtube.com/watch?v=D0b3C8le7Uo",
        "instructions": {
            "setup": "Stand with feet hip-width apart, arms at sides.",
            "execution": [
                "Drive your right knee up toward your chest",
                "Quickly switch and drive left knee up",
                "Pump your arms in opposition",
                "Stay on the balls of your feet",
                "Maintain a quick, running pace"
            ],
            "breathing": "Breathe rhythmically with the movement",
            "common_mistakes": [
                "Knees not coming high enough - Aim for waist height",
                "Leaning back - Stay upright or lean slightly forward",
                "Flat-footed - Stay on balls of feet",
                "Arms not moving - Pump arms for momentum"
            ],
            "tips": "Start slower to get the form, then increase speed. Great for warming up!"
        },
        "reps_range": "30-40 total",
        "sets_range": "3"
    },
    
    # ===== STRETCHING =====
    "standing_quad_stretch": {
        "name": "Standing Quad Stretch",
        "category": "Stretching",
        "muscle_groups": ["Quadriceps", "Hip Flexors"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Standing-Quad-Stretch.gif",
        "video_url": "https://www.youtube.com/watch?v=HaGbUlBHpwQ",
        "instructions": {
            "setup": "Stand tall on one leg, using a wall or chair for balance if needed.",
            "execution": [
                "Bend your right knee and grab your right foot behind you",
                "Pull your heel toward your glute",
                "Keep your knees close together",
                "Stand tall - don't lean forward",
                "Hold for 20-30 seconds, then switch"
            ],
            "breathing": "Breathe deeply and relax into the stretch",
            "common_mistakes": [
                "Knee drifting out - Keep knees together",
                "Leaning forward - Stand upright",
                "Arching back - Keep core engaged",
                "Holding breath - Breathe deeply"
            ],
            "tips": "Pull gently - you should feel a stretch, not pain. Hold something for balance if needed."
        },
        "reps_range": "20-30 seconds each leg",
        "sets_range": "2"
    },
    
    "cat_cow_stretch": {
        "name": "Cat-Cow Stretch",
        "category": "Stretching",
        "muscle_groups": ["Spine", "Core", "Back"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Cat-Stretch.gif",
        "video_url": "https://www.youtube.com/watch?v=kqnua4rHVVA",
        "instructions": {
            "setup": "Start on all fours with hands under shoulders and knees under hips.",
            "execution": [
                "COW: Drop belly toward floor, lift head and tailbone",
                "Arch your back gently",
                "CAT: Round your spine toward ceiling",
                "Tuck chin to chest and tailbone under",
                "Flow smoothly between positions"
            ],
            "breathing": "Inhale for cow, exhale for cat",
            "common_mistakes": [
                "Moving too fast - Go slow and feel each position",
                "Not using full range - Exaggerate both positions",
                "Holding breath - Sync breath with movement",
                "Straining neck - Keep movements gentle"
            ],
            "tips": "Great for warming up the spine! Move slowly and feel each vertebra."
        },
        "reps_range": "10 cycles",
        "sets_range": "2"
    },
    
    "childs_pose": {
        "name": "Child's Pose",
        "category": "Stretching",
        "muscle_groups": ["Back", "Hips", "Shoulders"],
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "gif_url": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Childs-Pose.gif",
        "video_url": "https://www.youtube.com/watch?v=2MJGg-dUKh0",
        "instructions": {
            "setup": "Kneel on the floor with big toes touching and knees apart.",
            "execution": [
                "Sit back on your heels",
                "Walk your hands forward on the floor",
                "Lower your forehead to the ground",
                "Let your belly rest between your thighs",
                "Relax and hold"
            ],
            "breathing": "Breathe deeply into your back",
            "common_mistakes": [
                "Butt not reaching heels - Open knees wider",
                "Shoulders tense - Let arms relax",
                "Holding breath - Breathe deeply",
                "Rushing - Take your time to relax"
            ],
            "tips": "Great rest position between exercises. Breathe deeply and let tension melt away."
        },
        "reps_range": "30-60 seconds",
        "sets_range": "1-2"
    }
}

# Exercise categories for filtering
EXERCISE_CATEGORIES = ["All", "Lower Body", "Upper Body", "Core", "Cardio", "Stretching"]

# Difficulty levels
DIFFICULTY_LEVELS = ["All", "Beginner", "Intermediate", "Advanced"]

# Mixamo 3D Character Resources
MIXAMO_RESOURCES = {
    "about": "Mixamo is Adobe's free service for 3D character animations. You can download rigged characters and animations for free!",
    "website": "https://www.mixamo.com/",
    "features": [
        "Free rigged 3D characters",
        "Hundreds of free animations",
        "Auto-rigging for your own characters",
        "FBX export for any 3D software",
        "Perfect for fitness app demonstrations"
    ],
    "recommended_characters": [
        {"name": "Y Bot", "description": "Gender-neutral robot - great for exercise demos", "url": "https://www.mixamo.com/#/?page=1&query=ybot"},
        {"name": "X Bot", "description": "Slim athletic robot character", "url": "https://www.mixamo.com/#/?page=1&query=xbot"},
        {"name": "Michelle", "description": "Female athletic character", "url": "https://www.mixamo.com/#/?page=1&query=michelle"},
        {"name": "Remy", "description": "Male athletic character", "url": "https://www.mixamo.com/#/?page=1&query=remy"}
    ],
    "fitness_animations": [
        "Standing Idle",
        "Walking",
        "Running",
        "Jumping",
        "Squatting",
        "Push Up",
        "Sit Up",
        "Stretching",
        "Boxing",
        "Kicking"
    ],
    "how_to_use": [
        "1. Go to mixamo.com and create a free Adobe account",
        "2. Browse characters and select one you like",
        "3. Browse animations and preview them on your character",
        "4. Download as FBX with 'With Skin' option",
        "5. Import into Blender, Unity, or Unreal Engine",
        "6. Use in your fitness app or videos!"
    ]
}

def get_exercise_by_name(name):
    """Get exercise details by name (case-insensitive)"""
    name_lower = name.lower().replace(" ", "_").replace("-", "_")
    return EXERCISE_LIBRARY.get(name_lower)

def get_exercises_by_category(category):
    """Get all exercises in a category"""
    if category == "All":
        return EXERCISE_LIBRARY
    return {k: v for k, v in EXERCISE_LIBRARY.items() if v["category"] == category}

def get_exercises_by_difficulty(difficulty):
    """Get all exercises by difficulty level"""
    if difficulty == "All":
        return EXERCISE_LIBRARY
    return {k: v for k, v in EXERCISE_LIBRARY.items() if v["difficulty"] == difficulty}

def get_exercises_by_muscle(muscle_group):
    """Get exercises targeting a specific muscle group"""
    return {k: v for k, v in EXERCISE_LIBRARY.items() if muscle_group in v["muscle_groups"]}

def search_exercises(query):
    """Search exercises by name or muscle group"""
    query = query.lower()
    results = {}
    for key, exercise in EXERCISE_LIBRARY.items():
        if (query in exercise["name"].lower() or 
            query in exercise["category"].lower() or
            any(query in muscle.lower() for muscle in exercise["muscle_groups"])):
            results[key] = exercise
    return results

def get_all_muscle_groups():
    """Get list of all unique muscle groups"""
    muscles = set()
    for exercise in EXERCISE_LIBRARY.values():
        muscles.update(exercise["muscle_groups"])
    return sorted(list(muscles))
