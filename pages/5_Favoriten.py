# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import requests
import csv
import io
import pandas as pd
from requests.auth import HTTPBasicAuth
from utils.theme import apply_theme

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Theme anwenden
apply_theme()

st.title("Ihre Favoriten 🍹")

# WebDAV-Zugangsdaten automatisch aus secrets
base_url = st.secrets["webdav"]["base_url"]
webdav_user = st.secrets["webdav"]["username"]
webdav_password = st.secrets["webdav"]["password"]

# Dynamischer Favoritenpfad pro Benutzer
remote_favoriten_url = f"{base_url}/files/{webdav_user}/trink_us/user_data_{webdav_user}/favoriten.csv"

# Favoriten laden
def favoriten_laden():
    try:
        response = requests.get(remote_favoriten_url, auth=HTTPBasicAuth(webdav_user, webdav_password))
        if response.status_code == 200:
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
    return []

# Favoriten speichern (z. B. nach Löschen)
def favoriten_speichern(favoriten_liste):
    try:
        if not favoriten_liste:
            csv_content = ""
        else:
            output = io.StringIO()
            fieldnames = favoriten_liste[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for fav in favoriten_liste:
                writer.writerow(fav)
            csv_content = output.getvalue()
        response = requests.put(
            remote_favoriten_url,
            data=csv_content.encode("utf-8"),
            headers={'Content-Type': 'text/csv'},
            auth=HTTPBasicAuth(webdav_user, webdav_password)
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")

favoriten = favoriten_laden()

if not favoriten:
    st.info("Noch keine Favoriten gespeichert.")
    st.stop()

# CSV-Export
csv_export = io.StringIO()
fieldnames = favoriten[0].keys()
writer = csv.DictWriter(csv_export, fieldnames=fieldnames)
writer.writeheader()
for eintrag in favoriten:
    writer.writerow(eintrag)

st.download_button(
    label="📤 Favoriten als CSV exportieren",
    data=csv_export.getvalue(),
    file_name="meine_favoriten.csv",
    mime="text/csv"
)

# Favoriten-Tabelle
df = pd.DataFrame(favoriten)
if not df.empty:
    df = df.sort_values('strDrink')
    st.dataframe(df[["strDrink", "strInstructions"] + [col for col in df.columns if col.startswith("strIngredient") or col.startswith("strMeasure") or col == "strDrinkThumb"]])

# Kartenansicht mit Löschen
st.markdown("---")
st.subheader("Favoriten als Karten")
cols = st.columns(3)

favoriten_geaendert = False
favoriten_neu = []

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

        # Löschbutton
        if st.button("❌ Aus Favoriten entfernen", key=f"del_{idx}"):
            favoriten_geaendert = True
            st.warning(f"'{rezept.get('strDrink')}' wird entfernt.")
        else:
            favoriten_neu.append(rezept)

# Nachträglich speichern, wenn sich etwas geändert hat
if favoriten_geaendert:
    favoriten_speichern(favoriten_neu)
    st.success("Favoriten wurden aktualisiert.")
    st.experimental_rerun()
