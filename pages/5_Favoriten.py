# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import os
import json
import streamlit as st
from utils.theme import apply_theme

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Theme anwenden
apply_theme()

# Titel der Seite
st.title("Ihre Favoriten 🍹")

# Pfad zur JSON-Datei für Favoriten
pages_folder = os.path.dirname(os.path.abspath(__file__))
favoriten_datei = os.path.join(pages_folder, "../favoriten.json")

# Favoriten aus der JSON-Datei laden
def favoriten_laden():
    if os.path.exists(favoriten_datei):
        with open(favoriten_datei, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                st.error("Fehler beim Laden der Favoriten. Die Datei ist beschädigt.")
                return []
    return []

# Favoriten initialisieren
favoriten = favoriten_laden()

# Gespeicherte Favoriten anzeigen
st.write("Ihre gespeicherten Rezepte:")
if favoriten:
    # Teile die Favoriten in 3 Spalten auf
    cols = st.columns(3)
    for index, rezept in enumerate(favoriten):
        # Wähle die aktuelle Spalte basierend auf dem Index
        col = cols[index % 3]
        with col:
            st.image(rezept["strDrinkThumb"], width=150)
            st.write(f"**{rezept['strDrink']}**")
            
            # Button für Details
            if st.button(f"zum Rezept", key=f"details_{index}"):
                st.write("Zutaten:")
                st.write("- 50ml Tequila")
                st.write("- 25ml Triple Sec")
                st.write("- 25ml Limettensaft")
                st.write("Zubereitung:")
                st.write("Alle Zutaten in einem Shaker mit Eis mischen. In ein Glas mit Salzrand abseihen.")
else:
    st.warning("Noch keine Favoriten gespeichert.")