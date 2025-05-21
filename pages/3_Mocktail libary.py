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

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Theme anwenden
apply_theme()

# Benutzername aus Login holen
username = st.session_state.get("username")
if not username:
    st.error("Bitte zuerst einloggen!")
    st.stop()

# WebDAV-Zugangsdaten
base_url = st.secrets["webdav"]["base_url"]
user = st.secrets["webdav"]["username"]
app_passwort = st.secrets["webdav"]["password"]

# 📁 Benutzerspezifischer Favoritenpfad
def get_favoriten_pfad(username):
    return f"{base_url}/files/{user}/trink_us/favoriten_{username}.csv"

# 📥 Favoriten laden
def favoriten_laden(username):
    url = get_favoriten_pfad(username)
    try:
        response = requests.get(url, auth=HTTPBasicAuth(user, app_passwort))
        if response.status_code == 200:
            reader = csv.DictReader(io.StringIO(response.text))
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
        return []

# 💾 Favoriten speichern
def favoriten_speichern(username, favoriten_liste):
    url = get_favoriten_pfad(username)
    output = io.StringIO()
    fieldnames = favoriten_liste[0].keys() if favoriten_liste else ["idDrink", "strDrink"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(favoriten_liste)
    try:
        response = requests.put(
            url,
            data=output.getvalue().encode("utf-8"),
            headers={"Content-Type": "text/csv"},
            auth=HTTPBasicAuth(user, app_passwort)
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Speichern fehlgeschlagen: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Favoriten: {e}")

# 🔎 Mocktails suchen
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

# 🔍 Details zu einem Mocktail
def mocktail_details(mocktail_id):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={mocktail_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("drinks", [])[0]
    else:
        st.error("Fehler beim Abrufen der Mocktail-Details.")
        return None

# CSS-Styling
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

# Titel & UI
st.title("🍹 Mocktail Library")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<label class="search-label">🔍 Suche nach einem Mocktail:</label>', unsafe_allow_html=True)
suchbegriff = st.text_input("", placeholder="Gib einen Mocktailnamen ein...")

# Favoriten initialisieren
favoriten = favoriten_laden(username)

# Anzeige der Suchergebnisse
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
            if st.button("Zu Favoriten hinzufügen", key=f"add_fav_{mocktail['idDrink']}"):
                if not any(fav.get("idDrink") == mocktail["idDrink"] for fav in favoriten):
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
                        favoriten_speichern(username, favoriten)
                        st.success(f"'{details['strDrink']}' wurde zu den Favoriten hinzugefügt!")
                else:
                    st.warning(f"'{mocktail['strDrink']}' ist bereits in den Favoriten.")
        st.markdown("---")
else:
    st.warning("Keine Mocktails gefunden. Bitte versuche es mit einem anderen Suchbegriff.")
