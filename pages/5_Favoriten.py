# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import os
import json
import streamlit as st

# Titel der Seite
st.title("Favoriten")

# Beschreibung
st.write("Hier können Sie Ihre Lieblingsrezepte speichern und verwalten.")

# Pfad zur JSON-Datei für Favoriten
pages_folder = os.path.dirname(os.path.abspath(__file__))
favoriten_datei = os.path.join(pages_folder, "../favoriten.json")

# Favoriten aus der JSON-Datei laden
def favoriten_laden():
    if os.path.exists(favoriten_datei):
        with open(favoriten_datei, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Favoriten initialisieren
favoriten = favoriten_laden()

# Gespeicherte Favoriten anzeigen
st.write("### Ihre gespeicherten Rezepte:")
if favoriten:
    for index, rezept in enumerate(favoriten):
        st.write(f"**{rezept['strDrink']}**")
        st.image(rezept["strDrinkThumb"], width=150)
        # Button für jedes Rezept
        if st.button(f"Details zu '{rezept['strDrink']}' anzeigen", key=f"details_{index}"):
            # Rezeptdetails anzeigen (Mock-Daten, da API keine Details liefert)
            st.write("### Zutaten:")
            st.write("- 50ml Tequila")
            st.write("- 25ml Triple Sec")
            st.write("- 25ml Limettensaft")
            st.write("### Zubereitung:")
            st.write("- Alle Zutaten in einem Shaker mit Eis mischen.")
            st.write("- In ein Glas mit Salzrand abseihen.")
        st.write("---")
else:
    st.write("Noch keine Favoriten gespeichert.")