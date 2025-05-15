# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from utils.theme import apply_theme

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Theme anwenden
apply_theme()

# ====== Hintergrundbild und Box-Design für beide Modi ======
image_url = "https://wallpapercave.com/wp/wp2361388.jpg"
if st.session_state["dark_mode"]:
    # Dark Mode: Bild mit dunklem Overlay
    bg_style = f"""
        background: linear-gradient(rgba(20,20,20,0.85), rgba(20,20,20,0.85)), url("{image_url}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    """
    main_bg = "rgba(30,30,30,0.85)"  # dunkler Bereich im Dark Mode
else:
    # Light Mode: Bild mit hellem Overlay
    bg_style = f"""
        background: linear-gradient(rgba(255,255,255,0.55), rgba(255,255,255,0.55)), url("{image_url}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    """
    main_bg = "rgba(255,255,255,0.85)"  # weißer Bereich im Light Mode

st.markdown(
    f"""
    <style>
    .stApp {{
        {bg_style}
    }}
    .main > div {{
        background-color: {main_bg};
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Mein Drink-Counter")

# Session-State initialisieren
if "drink_counts" not in st.session_state:
    st.session_state["drink_counts"] = {}

# Funktion zum Hinzufügen eines Drinks
def add_drink(drink_name):
    drink_name = drink_name.strip().title()
    if not drink_name:
        return
    if drink_name in st.session_state["drink_counts"]:
        st.session_state["drink_counts"][drink_name] += 1
    else:
        st.session_state["drink_counts"][drink_name] = 1

# Drink-Eingabe
drink_input = st.text_input("Wie heisst der Drink in deiner Hand ?")

# Button zum Hinzufügen aus Eingabefeld
if drink_input:
    if st.button("✅ Drink hinzufügen"):
        add_drink(drink_input)

# Buttons für bereits vorhandene Drinks
if st.session_state["drink_counts"]:
    st.markdown("### Bereits hinzugefügte Drinks:")
    for drink in st.session_state["drink_counts"]:
        if st.button(f"➕ {drink}"):
            add_drink(drink)

# Säulendiagramm anzeigen
if st.session_state["drink_counts"]:
    drinks = list(st.session_state["drink_counts"].keys())
    counts = list(st.session_state["drink_counts"].values())

    # Farben: "Set3" – freundlich und bunt/ "tab10" – klar und kontrastreich/ "Pastel1" – zart & hell/ "Accent" – lebendig
    cmap = cm.get_cmap("Pastel1", len(drinks)) 
    colors = [cmap(i) for i in range(len(drinks))]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(drinks, counts, color=colors)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    ax.set_yticks(range(0, max(counts) + 1))  # Ganze Zahlen auf Y-Achse
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("Noch keine Drinks hinzugefügt.")