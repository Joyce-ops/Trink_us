import streamlit as st
import requests
import io
import csv
from requests.auth import HTTPBasicAuth
import datetime

# WebDAV-Zugangsdaten aus Secrets
base_url = st.secrets["webdav"]["base_url"]
webdav_user = st.secrets["webdav"]["username"]
webdav_password = st.secrets["webdav"]["password"]

# Pfad für Benutzer-Favoriten
FAVORITEN_PFAD = f"{base_url}/files/{webdav_user}/trink_us/user_data_{webdav_user}/favoriten.csv"

# Favoriten laden
def favoriten_laden():
    try:
        response = requests.get(FAVORITEN_PFAD, auth=HTTPBasicAuth(webdav_user, webdav_password))
        if response.status_code == 200:
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
    return []

# Favoriten speichern
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
            FAVORITEN_PFAD,
            data=csv_content.encode("utf-8"),
            headers={'Content-Type': 'text/csv'},
            auth=HTTPBasicAuth(webdav_user, webdav_password)
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern der Favoriten: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Favoriten: {e}")

# Cocktail-API-Suche
def suche_cocktails(suchbegriff):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={suchbegriff}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("drinks", [])
    return []

# ---------------------- UI ----------------------
st.title("🍹 Cocktail Library")

with st.form("cocktail_suche_form"):
    suchbegriff = st.text_input("🔍 Suche nach einem Cocktail:", placeholder="Gib einen Namen ein...")
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
            if cocktail.get("strInstructions"):
                for idx, step in enumerate(cocktail["strInstructions"].split(". "), start=1):
                    if step.strip():
                        st.write(f"{idx}. {step.strip()}")
            else:
                st.write("Keine Anleitung verfügbar.")

            if st.button(f"⭐ Zu Favoriten: {cocktail['strDrink']}", key=f"fav_{cocktail['idDrink']}"):
                if not any(f.get("idDrink") == cocktail["idDrink"] for f in favoriten):
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
                    st.success(f"'{cocktail['strDrink']}' wurde zu deinen Favoriten gespeichert!")
                else:
                    st.warning(f"'{cocktail['strDrink']}' ist bereits in den Favoriten.")
    else:
        st.warning("Kein Cocktail gefunden.")
