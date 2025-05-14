import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

st.title("🥤 Deine persönliche Drink-Statistik")

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
drink_input = st.text_input("Gib einen Drink ein, den du konsumiert hast:")

# Button zum Hinzufügen aus dem Eingabefeld
if drink_input:
    if st.button("✅ Drink hinzufügen"):
        add_drink(drink_input)

# Buttons für bereits vorhandene Drinks
if st.session_state["drink_counts"]:
    st.markdown("### Bereits hinzugefügte Drinks:")
    for drink in st.session_state["drink_counts"]:
        if st.button(f"➕ {drink} erneut hinzufügen"):
            add_drink(drink)

# Säulendiagramm anzeigen
if st.session_state["drink_counts"]:
    drinks = list(st.session_state["drink_counts"].keys())
    counts = list(st.session_state["drink_counts"].values())

    # Zufällige Farben generieren
    colors = plt.cm.tab20(np.linspace(0, 1, len(drinks)))
    random.shuffle(colors)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(drinks, counts, color=colors)

    ax.set_xlabel("Drinks")
    ax.set_ylabel("Anzahl")
    ax.set_title("Drink-Häufigkeit")
    ax.set_yticks(range(0, max(counts) + 1))  # Nur ganze Zahlen auf der Y-Achse
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("Noch keine Drinks hinzugefügt.")
