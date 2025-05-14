import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

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
drink_input = st.text_input("Wie heißt der Drink, den du konsumierst?")

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

    # Farben aus schöner Colormap (z. B. tab20 oder Set3)
    cmap = cm.get_cmap("Set3", len(drinks))  # oder "tab10", "Pastel1", "Accent"
    colors = [cmap(i) for i in range(len(drinks))]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(drinks, counts, color=colors)

    ax.set_xlabel("Drink")
    ax.set_ylabel("Anzahl")
    ax.set_title("Häufigkeit deiner Drinks")
    ax.set_yticks(range(0, max(counts) + 1))  # Ganze Zahlen auf Y-Achse
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("Noch keine Drinks hinzugefügt.")
