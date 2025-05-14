import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import hashlib

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

# Funktion zur Farberzeugung pro Drink (konstant aus Name generiert)
def get_color_for_drink(drink_name):
    # Hash von Drink-Name → RGB-Wert
    h = int(hashlib.sha256(drink_name.encode()).hexdigest(), 16)
    r = (h & 0xFF0000) >> 16
    g = (h & 0x00FF00) >> 8
    b = h & 0x0000FF
    return (r / 255, g / 255, b / 255)

# Drink-Eingabe
drink_input = st.text_input("Wie heisst der Drink den du konsumierst?:")

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

    # Farben pro Drink
    colors = [get_color_for_drink(drink) for drink in drinks]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(drinks, counts, color=colors)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    ax.set_yticks(range(0, max(counts) + 1))  # Nur ganze Zahlen
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("Noch keine Drinks hinzugefügt.")
