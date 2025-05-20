# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('favoriten.py')
# ====== End Login Block ======

import streamlit as st
import requests
import csv
import io
import pandas as pd
from requests.auth import HTTPBasicAuth
from utils.theme import apply_theme

# Theme
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
apply_theme()

# Login prüfen
username = st.session_state.get("username")
if not username:
    st.error("Bitte zuerst einloggen!")
    st.stop()

# WebDAV-Zugang
base_url = st.secrets["webdav"]["base_url"]
user = st.secrets["webdav"]["username"]
password = st.secrets["webdav"]["password"]

# Pfad dynamisch
def get_favoriten_url(username):
    return f"{base_url}/files/{user}/trink_us/favoriten_{username}.csv"

# Laden
def favoriten_laden(username):
    try:
        response = requests.get(get_favoriten_url(username), auth=HTTPBasicAuth(user, password))
        if response.status_code == 200 and response.text.strip():
            return list(csv.DictReader(io.StringIO(response.text)))
    except Exception as e:
        st.error(f"Fehler beim Laden: {e}")
    return []

st.title("Ihre Favoriten 🍹")

favoriten = favoriten_laden(username)
if not favoriten:
    st.info("Noch keine Favoriten gespeichert.")
    st.stop()

# Tabelle
df = pd.DataFrame(favoriten)
df = df.sort_values('strDrink')
st.dataframe(df[["strDrink", "strInstructions"]])

# Kartenansicht
st.markdown("---")
st.subheader("Favoriten als Karten")
cols = st.columns(3)
for idx, rezept in enumerate(favoriten):
    col = cols[idx % 3]
    with col:
        if rezept.get("strDrinkThumb"):
            st.image(rezept["strDrinkThumb"], width=120)
        st.markdown(f"*{rezept.get('strDrink', 'Unbekannter Drink')}*")
        if st.button("Rezept anzeigen", key=f"details_{idx}"):
            zutaten = []
            for i in range(1, 16):
                zutat = rezept.get(f"strIngredient{i}")
                menge = rezept.get(f"strMeasure{i}")
                if zutat and zutat.strip():
                    zutaten.append(f"- {menge or ''} {zutat}".strip())
            if zutaten:
                st.markdown("*Zutaten:*")
                for z in zutaten:
                    st.markdown(z)
            st.markdown("*Zubereitung:*")
            st.write(rezept.get("strInstructions", "Keine Anleitung vorhanden."))
