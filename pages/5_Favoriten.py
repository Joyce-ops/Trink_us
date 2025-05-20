# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
import requests
import io
import csv
from requests.auth import HTTPBasicAuth
from utils.theme import apply_theme

# --- WebDAV Zugangsdaten ---
base_url = st.secrets["webdav"]["base_url"]
webdav_user = st.secrets["webdav"]["username"]
webdav_password = st.secrets["webdav"]["password"]

# --- Benutzername prüfen ---
username = st.session_state.get("username")
if not username:
    st.error("Bitte zuerst einloggen.")
    st.stop()

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

apply_theme()

st.title("Ihre Favoriten 🍹")

# --- Pfad zur benutzerspezifischen Datei ---
def get_favoriten_pfad(username):
    return f"{base_url}/files/{webdav_user}/trink_us/favoriten_{username}.csv"

# --- Favoriten laden ---
def favoriten_laden(username):
    url = get_favoriten_pfad(username)
    auth = HTTPBasicAuth(webdav_user, webdav_password)
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            content = response.content.decode("utf-8")
            reader = csv.DictReader(io.StringIO(content))
            return list(reader)
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
    return []

# --- Favoriten speichern ---
def favoriten_speichern(username, favoriten_liste):
    url = get_favoriten_pfad(username)
    auth = HTTPBasicAuth(webdav_user, webdav_password)

    if not favoriten_liste:
        csv_content = ""
    else:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=favoriten_liste[0].keys())
        writer.writeheader()
        writer.writerows(favoriten_liste)
        csv_content = output.getvalue()

    try:
        response = requests.put(
            url,
            data=csv_content.encode("utf-8"),
            headers={"Content-Type": "text/csv"},
            auth=auth
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Favoriten: {e}")

# --- Favoriten anzeigen ---
favoriten = favoriten_laden(username)

if not favoriten:
    st.info("Noch keine Favoriten gespeichert.")
    st.stop()

# Favoriten löschen
st.markdown("### Favoriten verwalten")
favoriten_ids = [f"{f['idDrink']} - {f['strDrink']}" for f in favoriten]
auswahl = st.multiselect("Favoriten zum Löschen auswählen:", favoriten_ids)

if st.button("Ausgewählte löschen"):
    favoriten = [f for f in favoriten if f"{f['idDrink']} - {f['strDrink']}" not in auswahl]
    favoriten_speichern(username, favoriten)
    st.success("Ausgewählte Favoriten wurden gelöscht.")
    st.experimental_rerun()

# CSV-Export
csv_download = pd.DataFrame(favoriten).to_csv(index=False).encode("utf-8")
st.download_button(
    label="📤 Favoriten als CSV herunterladen",
    data=csv_download,
    file_name="meine_favoriten.csv",
    mime="text/csv"
)

# Kartenanzeige
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
