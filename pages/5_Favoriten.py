# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import requests
import csv
import io
from requests.auth import HTTPBasicAuth
from utils.theme import apply_theme

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Theme anwenden
apply_theme()

st.title("Ihre Favoriten 🍹")

# WebDAV-Zugangsdaten
base_url = st.secrets["webdav"]["base_url"]
user = st.secrets["webdav"]["username"]
app_passwort = st.secrets["webdav"]["password"]
remote_favoriten_url = f"{base_url}/files/{user}/data.csv"

# Favoriten aus Switch Drive laden (CSV)
def favoriten_laden():
    try:
        response = requests.get(remote_favoriten_url, auth=HTTPBasicAuth(user, app_passwort))
        if response.status_code == 200:
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
        return []

# Favoriten laden
favoriten = favoriten_laden()

if not favoriten:
    st.info("Noch keine Favoriten gespeichert.")
    st.stop()

# Favoriten als Tabelle anzeigen (wie im BMI-Beispiel)
import pandas as pd
df = pd.DataFrame(favoriten)
if not df.empty:
    # Optional: Sortieren nach Name oder anderem Feld
    df = df.sort_values('strDrink')
    st.dataframe(df[["strDrink", "strInstructions"] + [col for col in df.columns if col.startswith("strIngredient") or col.startswith("strMeasure") or col == "strDrinkThumb"]])
else:
    st.info("Keine Favoriten vorhanden.")

# Optional: Bilder und Details in Spalten anzeigen
st.markdown("---")
st.subheader("Favoriten als Karten")
cols = st.columns(3)
for idx, rezept in enumerate(favoriten):
    col = cols[idx % 3]
    with col:
        if rezept.get("strDrinkThumb"):
            st.image(rezept["strDrinkThumb"], width=120)
        st.markdown(f"**{rezept.get('strDrink', 'Unbekannter Drink')}**")
        if st.button("Rezept anzeigen", key=f"details_{idx}"):
            zutaten = []
            for i in range(1, 16):
                zutat = rezept.get(f"strIngredient{i}")
                menge = rezept.get(f"strMeasure{i}")
                if zutat and zutat.strip():
                    zutaten.append(f"- {menge or ''} {zutat}".strip())
            if zutaten:
                st.markdown("**Zutaten:**")
                for z in zutaten:
                    st.markdown(z)
            st.markdown("**Zubereitung:**")
            st.write(rezept.get("strInstructions", "Keine Anleitung vorhanden."))