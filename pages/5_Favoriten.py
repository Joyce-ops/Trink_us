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

# Sicherstellen, dass die Favoriten-Daten vorhanden sind
if "fav_df" in st.session_state and not st.session_state.fav_df.empty:
    df = st.session_state.fav_df

    # Nur die Spalte mit Suchbegriffen
    if "Suchbegriff" in df.columns:
        # Schritt 1: Nur gültige, nicht-leere Einträge
        filtered_df = df[["Suchbegriff"]].dropna(subset=["Suchbegriff"])
        filtered_df = filtered_df[filtered_df["Suchbegriff"].str.strip() != ""]

        # Schritt 2: Hilfsspalte mit kleingeschriebener Version zur Duplikaterkennung
        filtered_df["suchbegriff_lower"] = filtered_df["Suchbegriff"].str.lower().str.strip()

        # Schritt 3: Gruppieren nach kleingeschriebener Form, und bevorzugt "richtige" Schreibweise behalten
        # Wir nehmen pro Gruppe den Suchbegriff mit Großbuchstaben (der zuerst vorkommt)
        grouped_df = (
            filtered_df.sort_values("Suchbegriff", ascending=False)
            .drop_duplicates(subset="suchbegriff_lower")
            .drop(columns="suchbegriff_lower")
        )

        # Schritt 4: Sortieren & Anzeigen
        grouped_df = grouped_df.sort_values("Suchbegriff").reset_index(drop=True)

        st.subheader("Einzigartige Suchbegriffe (nur korrekt geschriebene)")
        st.dataframe(grouped_df, use_container_width=True)
    else:
        st.warning("Die Spalte 'Suchbegriff' wurde nicht gefunden.")
else:
    st.info("Keine Favoriten gefunden.")
