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

# Favoriten in der JSON-Datei speichern
def favoriten_speichern(favoriten):
    with open(favoriten_datei, "w", encoding="utf-8") as file:
        json.dump(favoriten, file, ensure_ascii=False, indent=4)

# Favoriten-Liste initialisieren
if "favoriten" not in st.session_state:
    st.session_state["favoriten"] = favoriten_laden()

# Pfad zum Ordner mit den Rezepten
drinks_folder = os.path.join(pages_folder, "../drinks")

# Eingabefeld für neues Rezept
rezept_titel = st.text_input("Titel des Rezepts:")

# Automatisches Hinzufügen des Rezepts, wenn ein Titel eingegeben wird
if rezept_titel:
    # Überprüfen, ob das Rezept bereits existiert
    if not any(rezept["titel"] == rezept_titel for rezept in st.session_state["favoriten"]):
        # Rezept aus JSON-Datei laden
        rezept_datei = os.path.join(drinks_folder, rezept_titel, "rezept.json")
        if os.path.exists(rezept_datei):
            with open(rezept_datei, "r", encoding="utf-8") as file:
                rezept_inhalt = json.load(file)
            neues_rezept = {
                "titel": rezept_titel,
                "beschreibung": rezept_inhalt  # Das gesamte Rezept wird gespeichert
            }
            st.session_state["favoriten"].append(neues_rezept)
            favoriten_speichern(st.session_state["favoriten"])  # Favoriten speichern
            st.success(f"Rezept '{rezept_titel}' wurde hinzugefügt!")
        else:
            st.error(f"Kein Rezept für '{rezept_titel}' gefunden.")
    else:
        st.warning(f"Das Rezept '{rezept_titel}' ist bereits in den Favoriten gespeichert.")

# Gespeicherte Rezepte anzeigen
st.write("### Ihre gespeicherten Rezepte:")
if st.session_state["favoriten"]:
    for index, rezept in enumerate(st.session_state["favoriten"]):
        st.write(f"**{rezept['titel']}**")
        # Button für jedes Rezept
        if st.button(f"Details zu '{rezept['titel']}' anzeigen", key=f"details_{index}"):
            # Rezeptdetails anzeigen
            rezept_inhalt = rezept["beschreibung"]
            st.write("### Zutaten:")
            for zutat in rezept_inhalt["ingredients"]:
                st.write(f"- {zutat['amount']} {zutat['name']}")
            st.write("### Zubereitung:")
            for schritt in rezept_inhalt["instructions"]:
                st.write(f"- {schritt}")
        st.write("---")
else:
    st.write("Noch keine Favoriten gespeichert.")