# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import datetime
import streamlit as st
import requests
import io
import csv
from requests.auth import HTTPBasicAuth

# WebDAV-Zugangsdaten
base_url = st.secrets["webdav"]["base_url"]
user = st.secrets["webdav"]["username"]
app_passwort = st.secrets["webdav"]["password"]
remote_suchen_url = f"{base_url}/files/{user}/cocktail_suchen.csv"
remote_favoriten_url = f"{base_url}/files/{user}/favoriten.csv"

# Funktion: Suche laden
def suchen_laden():
    try:
        response = requests.get(remote_suchen_url, auth=HTTPBasicAuth(user, app_passwort))
        if response.status_code == 200:
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden der Suchhistorie: {e}")
        return []

# Funktion: Suche speichern
def suchen_speichern(suchen_liste):
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
            remote_suchen_url,
            data=csv_content.encode("utf-8"),
            headers={'Content-Type': 'text/csv'},
            auth=HTTPBasicAuth(user, app_passwort)
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern der Suchhistorie: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Suchhistorie: {e}")

# Funktion: Favoriten laden
def favoriten_laden():
    try:
        response = requests.get(remote_favoriten_url, auth=HTTPBasicAuth(user, app_passwort))
        if response.status_code == 200:
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
        return []

# Funktion: Favoriten speichern
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
            auth=HTTPBasicAuth(user, app_passwort)
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern der Favoriten: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Favoriten: {e}")

# Lade bisherige Suchen und Favoriten
suchen_liste = suchen_laden()
favoriten = favoriten_laden()

st.title("🍹 Cocktail Library")

# Funktion: Cocktails aus der API suchen
def suche_cocktails(suchbegriff):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={suchbegriff}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("drinks", [])
    else:
        st.error("Fehler beim Abrufen der Cocktails. Bitte versuche es später erneut.")
        return []

# Suchformular für Cocktails
with st.form("cocktail_suche_form"):
    suchbegriff = st.text_input("🔍 Suche nach einem Cocktail:", placeholder="Gib einen Cocktailnamen ein...")
    submitted = st.form_submit_button("Suchen")

if submitted and suchbegriff:
    # Suche speichern
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
                ingredient = cocktail.get(f"strIngredient{i}")
                measure = cocktail.get(f"strMeasure{i}")
                if ingredient:
                    st.write(f"- {measure or ''} {ingredient}")
            st.write("**Zubereitung:**")
            instructions = cocktail.get("strInstructions", "Keine Zubereitungsanweisungen verfügbar.")
            steps = instructions.split(". ")
            for idx, step in enumerate(steps, start=1):
                if step.strip():
                    st.write(f"{idx}. {step.strip()}")

            # Favoriten-Button unter jedem Rezept
            if st.button(f"Zu Favoriten speichern: {cocktail['strDrink']}", key=f"fav_{cocktail['idDrink']}"):
                # Prüfe, ob schon als Favorit vorhanden (nach idDrink)
                if not any(fav.get("idDrink") == cocktail["idDrink"] for fav in favoriten):
                    fav_dict = {
                        "idDrink": cocktail.get("idDrink"),
                        "strDrink": cocktail.get("strDrink"),
                        "strDrinkThumb": cocktail.get("strDrinkThumb"),
                        "strInstructions": cocktail.get("strInstructions"),
                    }
                    for i in range(1, 16):
                        fav_dict[f"strIngredient{i}"] = cocktail.get(f"strIngredient{i}")
                        fav_dict[f"strMeasure{i}"] = cocktail.get(f"strMeasure{i}")
                    favoriten.append(fav_dict)
                    favoriten_speichern(favoriten)
                    st.success(f"'{cocktail['strDrink']}' wurde zu den Favoriten hinzugefügt!")
                else:
                    st.warning(f"'{cocktail['strDrink']}' ist bereits in den Favoriten.")
    else:
        st.warning("Keine Cocktails gefunden. Bitte versuche es mit einem anderen Suchbegriff.")
elif not submitted:
    st.info("Gib einen Drink ein, um Cocktails zu finden.")

# Optional: Suchhistorie anzeigen
with st.expander("Suchhistorie anzeigen"):
    if suchen_liste:
        st.table(suchen_liste)
    else:
        st.write("Noch keine Suchen gespeichert.")