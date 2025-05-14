# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import os
import json
import streamlit as st

# Titel der Seite
st.title("🌟 Ihre Favoriten")

# Beschreibung
st.write("Hier können Sie Ihre Lieblingsrezepte speichern und verwalten.")

# CSS für die Gestaltung
favoriten_css = """
<style>
body {
    background-color: #f5f5f5; /* Helles Grau für den Hintergrund */
}
div[data-testid="stVerticalBlock"] {
    background-color: #000000; /* Schwarzer Hintergrund für die Box */
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    border-left: 5px solid #8fbf93; /* Grüner Akzent an der Seite */
}
h1, h2, h3, h4, h5, h6, p, div {
    color: #ffffff; /* Weißer Text */
}
button {
    background-color: #8fbf93 !important; /* Grüner Button */
    color: white !important; /* Weißer Text auf dem Button */
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 14px;
    cursor: pointer;
}
button:hover {
    background-color: #7aad84 !important; /* Dunkleres Grün beim Hover */
}
</style>
"""

# CSS in Streamlit einfügen
st.markdown(favoriten_css, unsafe_allow_html=True)

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
st.write("### Ihre gespeicherten Rezepte:")
if favoriten:
    for index, rezept in enumerate(favoriten):
        with st.container():
            st.markdown(f"**{rezept['strDrink']}**")
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
    st.warning("Noch keine Favoriten gespeichert.")