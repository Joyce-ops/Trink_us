import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


import streamlit as st

# Funktion: CSS für einen weich überlagerten Hintergrund
def set_faded_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)),
                        url("{image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }}

        .main > div {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Dein neues Hintergrundbild (Mocktails)
image_url = "https://wallpapercave.com/wp/wp2361388.jpg"

# Hintergrund anwenden
set_faded_background(image_url)

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
drink_input = st.text_input("Wie heißt der Drink in deiner Hand ?")

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
    cmap = cm.get_cmap("Accent", len(drinks))  # oder "tab10", "Pastel1", "Accent"
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
