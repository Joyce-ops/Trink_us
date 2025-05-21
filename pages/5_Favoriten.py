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

if "fav_df" in st.session_state and not st.session_state.fav_df.empty:
    df = st.session_state.fav_df.copy()

    if "Suchbegriff" in df.columns:
        # Nur gültige, nicht-leere Einträge behalten
        filtered_df = df[df["Suchbegriff"].notna() & (df["Suchbegriff"].str.strip() != "")].copy()

        # Hilfsspalte mit kleingeschriebener Version für Duplikaterkennung
        filtered_df["suchbegriff_lower"] = filtered_df["Suchbegriff"].str.lower().str.strip()

        # Gruppieren und die bevorzugte Version behalten (hier: alphabetisch größte Version)
        filtered_df = filtered_df.sort_values("Suchbegriff", ascending=False)
        grouped_df = filtered_df.drop_duplicates(subset="suchbegriff_lower", keep="first")

        # Spalte für Anzeige sortieren und index zurücksetzen
        grouped_df = grouped_df.drop(columns="suchbegriff_lower").sort_values("Suchbegriff").reset_index(drop=True)

        st.subheader("Einzigartige Suchbegriffe (Groß-/Kleinschreibung berücksichtigt, klein geschriebene entfernt)")
        st.dataframe(grouped_df[["Suchbegriff"]], use_container_width=True)
    else:
        st.warning("Die Spalte 'Suchbegriff' wurde nicht gefunden.")
else:
    st.info("Keine Favoriten gefunden.")

