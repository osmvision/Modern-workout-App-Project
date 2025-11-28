# 💎 Jade Fitness Hub

A beautiful, futuristic fitness app designed for Jade with a stunning blue theme.

![Jade Fitness Hub](https://img.shields.io/badge/Made%20with-💙-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

## ✨ Features

### 🏠 Home Dashboard
- Personalized greeting based on time of day
- Today's scheduled workouts with completion tracking
- Weekly progress overview
- Daily motivational quotes

### 📅 Workout Calendar
- Interactive monthly calendar view
- Schedule workouts for any date
- Track completed vs pending workouts
- Add notes and duration to each workout
- Visual indicators for scheduled days

### 💪 Workout Programs
Curated workout programs designed for women:

1. **💪 Beginner Full Body Tone** - 4 weeks, 3 days/week
2. **🍑 Slim Thick Program** - 6 weeks, 4 days/week (Glutes & Waist focus)
3. **🧘 Yoga & Flexibility Flow** - 4 weeks, 5 days/week
4. **🔥 HIIT Fat Burner** - 4 weeks, 4 days/week
5. **🍑 30 Day Booty Builder** - 30 days, 6 days/week

### 🎬 Video Collection
- Save YouTube workout videos
- Categorize by workout type
- Filter and browse your collection
- Watch videos directly in the app

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jade_fitness_project.git
cd jade_fitness_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free!)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and `app.py`
6. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app`

### Option 2: Cloudflare Pages with Workers

Since Streamlit requires a Python backend, you'll need Cloudflare Workers for full deployment:

1. **Create a Cloudflare account** at [cloudflare.com](https://cloudflare.com)

2. **Install Wrangler CLI:**
```bash
npm install -g wrangler
```

3. **Login to Cloudflare:**
```bash
wrangler login
```

4. **Deploy using Docker + Cloudflare Tunnel:**
   - This requires Cloudflare Tunnel for the Python backend
   - See Cloudflare's documentation for Python app deployment

### Option 3: Railway (Easy Python Hosting)

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway auto-detects Streamlit apps
4. Your app deploys automatically!

### Option 4: Render

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Option 5: Heroku

1. Create `Procfile`:
```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

3. Deploy to Heroku:
```bash
heroku create jade-fitness-hub
git push heroku main
```

## 📁 Project Structure

```
jade_fitness_project/
├── app.py                 # Main Streamlit application
├── utils.py               # Utility functions & workout programs
├── requirements.txt       # Python dependencies
├── workouts.csv          # Saved workout videos
├── workout_calendar.json # Calendar data
└── README.md             # This file
```

## 🎨 Customization

### Change the Theme
Edit the CSS in `app.py` to customize:
- Background colors
- Accent colors (currently cyan/blue)
- Fonts
- Animations

### Add More Programs
Edit `utils.py` and add new programs to the `GIRLS_WORKOUT_PROGRAMS` dictionary.

## 🤝 Contributing

Feel free to fork this project and make it your own!

## 📄 License

This project is open source and available under the MIT License.

---

<p align="center">Made with 💙 for Jade | Stay Strong, Stay Beautiful ✨</p>
