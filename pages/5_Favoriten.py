import streamlit as st
import pandas as pd
import requests
import io
import csv
from requests.auth import HTTPBasicAuth

# Login
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 

username = st.session_state.get("username")
if not username:
    st.stop()

# WebDAV
base_url = st.secrets["webdav"]["base_url"]
webdav_user = st.secrets["webdav"]["username"]
webdav_password = st.secrets["webdav"]["password"]
user_path = f"{base_url}/trink_us/user_data_{username}/data.csv"
auth = HTTPBasicAuth(webdav_user, webdav_password)

# Favoriten laden
def favoriten_laden():
    try:
        response = requests.get(user_path, auth=auth)
        if response.status_code == 200:
            content = io.StringIO(response.text)
            return list(csv.DictReader(content))
    except:
        pass
    return []

# Favoriten speichern
def favoriten_speichern(favs):
    try:
        if not favs:
            data = ""
        else:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=favs[0].keys())
            writer.writeheader()
            writer.writerows(favs)
            data = output.getvalue()
        requests.put(user_path, data=data.encode("utf-8"), auth=auth)
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")

# UI
st.title("Ihre Favoriten 🍹")
favoriten = favoriten_laden()

if not favoriten:
    st.info("Noch keine Favoriten gespeichert.")
    st.stop()

st.markdown("### Favoriten verwalten")
auswahl = st.multiselect("Favoriten löschen:", [f"{f['idDrink']} - {f['strDrink']}" for f in favoriten])

if st.button("Ausgewählte löschen"):
    favoriten = [f for f in favoriten if f"{f['idDrink']} - {f['strDrink']}" not in auswahl]
    favoriten_speichern(favoriten)
    st.success("Favoriten gelöscht.")
    st.experimental_rerun()

# Download
csv_download = pd.DataFrame(favoriten).to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV herunterladen", csv_download, "data.csv", "text/csv")

# Anzeige als Karten
st.subheader("Favoriten als Karten")
cols = st.columns(3)
for idx, rezept in enumerate(favoriten):
    col = cols[idx % 3]
    with col:
        if rezept.get("strDrinkThumb"):
            st.image(rezept["strDrinkThumb"], width=120)
        st.markdown(f"**{rezept.get('strDrink', 'Unbekannter Drink')}**")
        if st.button("Details anzeigen", key=f"details_{idx}"):
            zutaten = []
            for i in range(1, 16):
                zutat = rezept.get(f"strIngredient{i}")
                menge = rezept.get(f"strMeasure{i}")
                if zutat:
                    zutaten.append(f"- {menge or ''} {zutat}".strip())
            if zutaten:
                st.markdown("**Zutaten:**")
                for z in zutaten:
                    st.markdown(z)
            st.markdown("**Zubereitung:**")
            st.write(rezept.get("strInstructions", "Keine Anleitung"))
