# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ====== 

from utils.data_manager import DataManager
from utils.helpers import ch_now

import streamlit as st
import requests
import io
import csv
from requests.auth import HTTPBasicAuth

# WebDAV Zugangsdaten
base_url = st.secrets["webdav"]["base_url"]
webdav_user = st.secrets["webdav"]["username"]
webdav_password = st.secrets["webdav"]["password"]

# Benutzername aus Login
username = st.session_state.get("username")
if not username:
    st.error("Bitte zuerst einloggen!")
    st.stop()

#nochmals anschauen
# 🔁 Favoriten-Pfad (benutzerspezifisch)
def get_favoriten_pfad(username):
    return f"{base_url}/files/{webdav_user}/trink_us/favoriten_{username}.csv"

# 🔁 Favoriten laden
def favoriten_laden(username):
    url = get_favoriten_pfad(username)
    auth = HTTPBasicAuth(webdav_user, webdav_password)
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            reader = csv.DictReader(io.StringIO(response.text))
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden: {e}")
        return []

# 🔁 Favoriten speichern
def favoriten_speichern(username, favoriten_liste):
    url = get_favoriten_pfad(username)
    auth = HTTPBasicAuth(webdav_user, webdav_password)
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
            auth=auth
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Speichern fehlgeschlagen: {response.status_code}")
    except Exception as e:
        st.error(f"Speicherfehler: {e}")

# Cocktail-API-Suche
def suche_cocktails(suchbegriff):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={suchbegriff}"
    response = requests.get(url)
    if response.status_code == 200:

        return response.json().get("drinks", [])
    return []

# UI
st.title("🍹 Cocktail Library")


with st.form("cocktail_suche_form"):
    suchbegriff = st.text_input("🔍 Suche nach einem Cocktail:", placeholder="Gib einen Namen ein...")
    submitted = st.form_submit_button("Suchen")

if submitted and suchbegriff:
    cocktails = suche_cocktails(suchbegriff)
    st.session_state["cocktails"] = cocktails

if "cocktails" in st.session_state:
    cocktails = st.session_state["cocktails"]

    record = {
        "timestamp":ch_now(),
        "Suchbegriff": suchbegriff
    }
    DataManager().append_record('fav_df', record)

    favoriten = favoriten_laden(username)

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

            # ⭐ Favoriten-Button
            if st.button(f"⭐ Zu Favoriten hinzufügen", key=f"fav_{cocktail['idDrink']}"):
                record = {
                    "timestamp":ch_now(),
                    "Suchbegriff": cocktail['strDrink']
                }
                DataManager().append_record('fav_df', record)
                print(f"Saved: {cocktail['strDrink']}")

                # -------------
                if not any(f.get("idDrink") == cocktail["idDrink"] for f in favoriten):
                    fav_dict = {
                        "idDrink": cocktail["idDrink"],
                        "strDrink": cocktail["strDrink"],
                        "strDrinkThumb": cocktail["strDrinkThumb"],
                        "strInstructions": cocktail["strInstructions"] or "",
                    }
                    for i in range(1, 16):
                        fav_dict[f"strIngredient{i}"] = cocktail.get(f"strIngredient{i}") or ""
                        fav_dict[f"strMeasure{i}"] = cocktail.get(f"strMeasure{i}") or ""
                    favoriten.append(fav_dict)
                    favoriten_speichern(username, favoriten)
                    st.success(f"'{cocktail['strDrink']}' wurde gespeichert!")
                else:
                    st.warning(f"'{cocktail['strDrink']}' ist bereits gespeichert.")
    else:






























































































































        st.warning("Kein Cocktail gefunden.")
