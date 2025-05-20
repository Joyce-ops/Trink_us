import datetime
import streamlit as st
import requests
import io
import csv
from requests.auth import HTTPBasicAuth

# WebDAV-Zugangsdaten
base_url = st.secrets["webdav"]["base_url"]
webdav_user = st.secrets["webdav"]["username"]
webdav_password = st.secrets["webdav"]["password"]

# Benutzername Login
username = st.text_input("🔐 Benutzername", key="username")

def get_user_favoriten_url():
    if not username:
        return None
    return f"{base_url}/files/{webdav_user}/trink_us/user_data_{username}/favoriten.csv"

def get_user_suchen_url():
    if not username:
        return None
    return f"{base_url}/files/{webdav_user}/trink_us/user_data_{username}/cocktail_suchen.csv"

# Favoriten laden
def favoriten_laden():
    url = get_user_favoriten_url()
    if not url:
        return []
    try:
        response = requests.get(url, auth=HTTPBasicAuth(webdav_user, webdav_password))
        if response.status_code == 200:
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
        return []

# Favoriten speichern
def favoriten_speichern(favoriten_liste):
    url = get_user_favoriten_url()
    if not url:
        return
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
            url,
            data=csv_content.encode("utf-8"),
            headers={'Content-Type': 'text/csv'},
            auth=HTTPBasicAuth(webdav_user, webdav_password)
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern der Favoriten: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Favoriten: {e}")

# Suchen laden/speichern (optional)
def suchen_laden():
    url = get_user_suchen_url()
    if not url:
        return []
    try:
        response = requests.get(url, auth=HTTPBasicAuth(webdav_user, webdav_password))
        if response.status_code == 200:
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden der Suchhistorie: {e}")
        return []

def suchen_speichern(suchen_liste):
    url = get_user_suchen_url()
    if not url:
        return
    try:
        if not suchen_liste:
            csv_content = ""
        else:
            output = io.StringIO()
            fieldnames = suchen_liste[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for eintrag in suchen_liste:
                writer.writerow(eintrag)
            csv_content = output.getvalue()
        response = requests.put(
            url,
            data=csv_content.encode("utf-8"),
            headers={'Content-Type': 'text/csv'},
            auth=HTTPBasicAuth(webdav_user, webdav_password)
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern der Suchhistorie: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Suchhistorie: {e}")

# ------------------- Hauptanwendung -------------------

st.title("🍹 Cocktail Library")

if username:
    favoriten = favoriten_laden()
    suchen_liste = suchen_laden()

    def suche_cocktails(suchbegriff):
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={suchbegriff}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("drinks", [])
        return []

    # Suchformular
    with st.form("cocktail_suche_form"):
        suchbegriff = st.text_input("🔍 Suche nach einem Cocktail:")
        submitted = st.form_submit_button("Suchen")

    if submitted and suchbegriff:
        suchen_liste.append({
            "suchbegriff": suchbegriff,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        suchen_speichern(suchen_liste)

        cocktails = suche_cocktails(suchbegriff)
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
                instruktionen = cocktail.get("strInstructions", "Keine Angaben.")
                steps = instruktionen.split(". ")
                for idx, step in enumerate(steps, start=1):
                    if step.strip():
                        st.write(f"{idx}. {step.strip()}")

                if st.button(f"⭐ Favorit: {cocktail['strDrink']}", key=f"fav_{cocktail['idDrink']}"):
                    if not any(fav.get("idDrink") == cocktail["idDrink"] for fav in favoriten):
                        fav_dict = {
                            "idDrink": cocktail["idDrink"],
                            "strDrink": cocktail["strDrink"],
                            "strDrinkThumb": cocktail["strDrinkThumb"],
                            "strInstructions": cocktail["strInstructions"],
                        }
                        for i in range(1, 16):
                            fav_dict[f"strIngredient{i}"] = cocktail.get(f"strIngredient{i}")
                            fav_dict[f"strMeasure{i}"] = cocktail.get(f"strMeasure{i}")
                        favoriten.append(fav_dict)
                        favoriten_speichern(favoriten)
                        st.success(f"'{cocktail['strDrink']}' wurde zu deinen Favoriten hinzugefügt!")
                    else:
                        st.warning(f"'{cocktail['strDrink']}' ist bereits in deinen Favoriten.")
        else:
            st.warning("Kein Cocktail gefunden.")
    elif not submitted:
        st.info("Gib einen Cocktailnamen ein, um zu starten.")

    with st.expander("📜 Suchhistorie anzeigen"):
        if suchen_liste:
            st.table(suchen_liste)
        else:
            st.write("Keine gespeicherten Suchbegriffe.")

    with st.expander("⭐ Meine Favoriten"):
        if favoriten:
            for fav in favoriten:
                st.markdown(f"**{fav['strDrink']}**")
                st.image(fav["strDrinkThumb"], width=120)
        else:
            st.info("Noch keine Favoriten gespeichert.")
else:
    st.warning("Bitte gib deinen Benutzernamen ein, um deine Favoriten zu speichern.")