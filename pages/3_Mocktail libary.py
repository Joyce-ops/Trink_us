# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import requests
import streamlit as st
import io
import csv
from requests.auth import HTTPBasicAuth
from utils.theme import apply_theme
from utils.data_manager import DataManager
from utils.helpers import ch_now

st.title("🍹 Mocktail Library")

# WebDAV-Zugangsdaten
base_url = st.secrets["webdav"]["base_url"]
user = st.secrets["webdav"]["username"]
app_passwort = st.secrets["webdav"]["password"]
remote_favoriten_url = f"{base_url}/files/{user}/mocktail_favoriten.csv"

# Favoriten aus Switch Drive laden (CSV)
def favoriten_laden():
    try:
        response = requests.get(remote_favoriten_url, auth=HTTPBasicAuth(user, app_passwort))
        if response.status_code == 200 and response.text.strip():
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
        return []

# Favoriten als CSV speichern
def favoriten_speichern(favoriten):
    try:
        if not favoriten:
            csv_content = ""
        else:
            output = io.StringIO()
            fieldnames = favoriten[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for fav in favoriten:
                writer.writerow(fav)
            csv_content = output.getvalue()
        response = requests.put(
            remote_favoriten_url,
            data=csv_content.encode("utf-8"),
            headers={"Content-Type": "text/csv"},
            auth=HTTPBasicAuth(user, app_passwort)
        )
        if response.status_code not in (200, 201, 204):
            st.error(f"Fehler beim Speichern der Favoriten: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Favoriten: {e}")

# Favoriten initialisieren
favoriten = favoriten_laden()

# Funktion: Mocktails aus der API suchen
def suche_mocktails(suchbegriff=None):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        drinks = data.get("drinks", [])
        if suchbegriff:
            return [drink for drink in drinks if suchbegriff.lower() in drink["strDrink"].lower()]
        return drinks
    else:
        st.error("Fehler beim Abrufen der Mocktails. Bitte versuche es später erneut.")
        return []

# Funktion: Details eines Mocktails abrufen
def mocktail_details(mocktail_id):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={mocktail_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("drinks", [])[0]
    else:
        st.error("Fehler beim Abrufen der Mocktail-Details. Bitte versuche es später erneut.")
        return None

# CSS für größere Mocktail-Namen und zentrierte Rezepttexte (kein Hintergrund!)
st.markdown(
    """
    <style>
    div[data-testid="stButton"] > button {
        font-size: 12px;
    }
    .mocktail-name {
        font-size: 22px;
        margin-top: 5px;
        margin-bottom: 5px;
        text-align: center;
        font-weight: bold;
    }
    .recipe-text {
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: 5px;
        text-align: center;
    }
    .stTextInput > div > div:first-child {
        margin-bottom: 0px;
    }
    .recipe-spacing {
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.form("cocktail_suche_form"):
    suchbegriff = st.text_input("🔍 Suche nach einem Cocktail:", placeholder="Gib einen Mocktailnamen ein...")
    submitted = st.form_submit_button("Suchen")

# Username aus Session holen
username = st.session_state.get("username", user)

# Mocktails suchen und anzeigen
mocktails = suche_mocktails(suchbegriff)
if mocktails:
    st.subheader("Mocktail Vorschläge ✨")
    for idx, mocktail in enumerate(mocktails):
        col1, col2, col3 = st.columns([1, 3, 3])
        with col1:
            st.image(mocktail["strDrinkThumb"], width=100)
        with col2:
            st.markdown(f"<p class='mocktail-name'>{mocktail['strDrink']}</p>", unsafe_allow_html=True)
        with col3:
            if st.button("Rezept anzeigen", key=f"details_{mocktail['idDrink']}"):
                details = mocktail_details(mocktail["idDrink"])
                if details:
                    with col2:
                        st.markdown("<div class='recipe-spacing'></div>", unsafe_allow_html=True)
                        st.markdown("<p class='recipe-text'><b>Zutaten:</b></p>", unsafe_allow_html=True)
                        for i in range(1, 16):
                            ingredient = details.get(f"strIngredient{i}")
                            measure = details.get(f"strMeasure{i}")
                            if ingredient:
                                st.markdown(f"<p class='recipe-text'>- {measure or ''} {ingredient}</p>", unsafe_allow_html=True)
                        st.markdown("<p class='recipe-text'><b>Zubereitung:</b></p>", unsafe_allow_html=True)
                        st.markdown(f"<p class='recipe-text'>{details.get('strInstructions', 'Keine Zubereitungsanweisungen verfügbar.')}</p>", unsafe_allow_html=True)
            # ⭐ Favoriten-Button
            if st.button(f"⭐ Zu Favoriten hinzufügen", key=f"fav_{mocktail['idDrink']}"):
                # Lokale Favoritenverwaltung (DataFrame oder Liste)
                record = {
                    "timestamp": ch_now(),
                    "Suchbegriff": mocktail['strDrink']
                }
                DataManager().append_record('fav_df', record)
                # WebDAV-Favoriten
                if not any(f.get("idDrink") == mocktail["idDrink"] for f in favoriten):
                    details = mocktail_details(mocktail["idDrink"])
                    if details:
                        fav_dict = {
                            "idDrink": details.get("idDrink"),
                            "strDrink": details.get("strDrink"),
                            "strDrinkThumb": details.get("strDrinkThumb"),
                            "strInstructions": details.get("strInstructions") or "",
                        }
                        for i in range(1, 16):
                            fav_dict[f"strIngredient{i}"] = details.get(f"strIngredient{i}") or ""
                            fav_dict[f"strMeasure{i}"] = details.get(f"strMeasure{i}") or ""
                        favoriten.append(fav_dict)
                        favoriten_speichern(favoriten)
                        st.success(f"'{details['strDrink']}' wurde gespeichert!")
                else:
                    st.warning(f"'{mocktail['strDrink']}' ist bereits gespeichert.")
        st.markdown("---")
else:
    st.warning("Keine Mocktails gefunden. Bitte versuche es mit einem anderen Suchbegriff.")