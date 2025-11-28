import pandas as pd
import smtplib
import random
import datetime

# LOAD YOUR DB
df = pd.read_csv('workouts.csv')

# PICK RANDOM
if not df.empty:
    workout = df.sample().iloc[0]
    
    # EMAIL CONFIG (Use App Password from Google)
    EMAIL_ADDRESS = "your_email@gmail.com"
    EMAIL_PASSWORD = "your_app_password"
    
    msg = f"Subject: Daily Workout: {workout['title']}\n\nHere is your workout for today: {workout['url']}"
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
        print("Email sent!")