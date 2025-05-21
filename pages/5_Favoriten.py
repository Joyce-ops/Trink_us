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

# Titel
st.title("Ihre Favoriten 🍹")

# ------------------------------
# Duplikate entfernen nach strDrink (kann angepasst werden)
# ------------------------------
if "fav_df" in st.session_state:
    df = st.session_state.fav_df.copy()

    # Duplikate entfernen – z. B. nach strDrink
    df = df.drop_duplicates(subset="suchbegriff", keep="first")

    # Optional: sortieren
    df = df.sort_values("strDrinksuchbegriff")

    # Aktualisieren, wenn du es brauchst:
    # st.session_state.fav_df = df

    # Anzeige
    st.dataframe(df, use_container_width=True)
else:
    st.info("Keine Favoriten gefunden.")
