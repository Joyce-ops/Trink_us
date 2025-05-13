# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import requests

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        data = response.json()
        temp = data["current_condition"][0]["temp_C"]
        weather_desc = data["current_condition"][0]["weatherDesc"][0]["value"]
        return float(temp), weather_desc
    except Exception as e:
        return None, f"Fehler: {e}"

def recommend_cocktail(temp):
    if temp >= 25:
        return "🌞 Mojito – perfekt für heiße Tage!"
    elif 15 <= temp < 25:
        return "🍹 Whiskey Sour – angenehm frisch und ausgewogen."
    else:
        return "🔥 Hot Toddy – wärmt von innen!"

st.title("🍸 Standortbasierte Cocktail-Empfehlung")
city = st.text_input("Gib deine Stadt ein:")

if city:
    temp, weather = get_weather(city)
    if temp is not None:
        st.write(f"🌡️ Temperatur in {city}: {temp}°C")
        st.write(f"☁️ Wetter: {weather}")
        st.success(recommend_cocktail(temp))
    else:
        st.error(f"❌ {weather}")
