import streamlit as st
import requests
import io
import csv
from requests.auth import HTTPBasicAuth

# Login prüfen
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 

username = st.session_state.get("username")
if not username:
    st.stop()

# WebDAV-Daten
base_url = st.secrets["webdav"]["base_url"]
webdav_user = st.secrets["webdav"]["username"]
webdav_password = st.secrets["webdav"]["password"]

# Benutzerpfad
user_path = f"{base_url}/trink_us/user_data_{username}/favoriten.csv"
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
        response = requests.put(user_path, data=data.encode("utf-8"), headers={'Content-Type': 'text/csv'}, auth=auth)
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler: {e}")

# Suche
def suche_cocktails(suchbegriff):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={suchbegriff}"
    resp = requests.get(url)
    return resp.json().get("drinks", []) if resp.status_code == 200 else []

st.title("🍹 Cocktail Library")

with st.form("search_form"):
    suchbegriff = st.text_input("🔍 Cocktail suchen", placeholder="z. B. Mojito")
    submitted = st.form_submit_button("Suchen")

if submitted and suchbegriff:
    cocktails = suche_cocktails(suchbegriff)
    favoriten = favoriten_laden()

    if cocktails:
        for cocktail in cocktails:
            st.markdown(f"### {cocktail['strDrink']}")
            st.image(cocktail["strDrinkThumb"], width=150)

            st.write("**Zutaten:**")
            for i in range(1, 16):
                zutat = cocktail.get(f"strIngredient{i}")
                menge = cocktail.get(f"strMeasure{i}")
                if zutat:
                    st.write(f"- {menge or ''} {zutat}")

            st.write("**Zubereitung:**")
            st.write(cocktail.get("strInstructions", "Keine Anleitung vorhanden."))

            if st.button(f"⭐ Zu Favoriten: {cocktail['strDrink']}", key=f"fav_{cocktail['idDrink']}"):
                if not any(f.get("idDrink") == cocktail["idDrink"] for f in favoriten):
                    fav = {k: cocktail.get(k) for k in cocktail.keys()}
                    favoriten.append(fav)
                    favoriten_speichern(favoriten)
                    st.success(f"{cocktail['strDrink']} wurde gespeichert!")
                else:
                    st.info("Bereits in Favoriten")
    else:
        st.warning("Keine Cocktails gefunden.")
