# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import requests
from utils.theme import apply_theme

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Theme anwenden
apply_theme()

# ====== Hintergrundbild je nach Modus ======
image_url = "https://img.freepik.com/premium-photo/sky-different-weather-collage-generative-ai_169016-36937.jpg"
if st.session_state["dark_mode"]:
    overlay = "linear-gradient(rgba(20,20,20,0.85), rgba(20,20,20,0.85))"
else:
    overlay = "linear-gradient(rgba(255,255,255,0.55), rgba(255,255,255,0.55))"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {overlay}, url("{image_url}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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
        return "Mojito", "🌞 Mojito – perfekt für heiße Tage!"
    elif 15 <= temp < 25:
        return "Whiskey Sour", "🍹 Whiskey Sour – angenehm frisch und ausgewogen."
    else:
        return "Hot Toddy", "🔥 Hot Toddy – wärmt von innen!"

def show_cocktail_recipe(cocktail_name):
    recipes = {
        "Mojito": """
        **Rezept für Mojito:**
        - 50 ml weißer Rum
        - 1 Limette
        - 2 TL Zucker
        - Minzblätter
        - Soda Water
        - Eiswürfel
        """,
        "Whiskey Sour": """
        **Rezept für Whiskey Sour:**
        - 50 ml Whiskey
        - 25 ml Zitronensaft
        - 15 ml Zuckersirup
        - Eiswürfel
        - Optional: Eiweiß
        """,
        "Hot Toddy": """
        **Rezept für Hot Toddy:**
        - 50 ml Whiskey
        - 1 EL Honig
        - 1 EL Zitronensaft
        - Heißes Wasser
        - Optional: Zimtstange
        """
    }
    return recipes.get(cocktail_name, "Rezept nicht verfügbar.")

st.title("🍸 Standortbasierte Cocktail-Empfehlung")
city = st.text_input("Gib deine Stadt ein:")

if city:
    temp, weather = get_weather(city)
    if temp is not None:
        st.write(f"🌡️ Temperatur in {city}: {temp}°C")
        st.write(f"☁️ Wetter: {weather}")
        
        # Cocktail-Empfehlung
        cocktail_name, recommendation = recommend_cocktail(temp)
        st.success(recommendation)
        
        # Button für das Rezept
        if st.button(f"📖 Rezept für {cocktail_name} anzeigen"):
            st.markdown(show_cocktail_recipe(cocktail_name))
    else:
        st.error(f"❌ {weather}")