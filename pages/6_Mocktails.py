import requests
import streamlit as st

# Streamlit-Seitenkonfiguration
st.set_page_config(page_title="Mocktail-Rezepte", page_icon="🍹")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

# API-URL (Mocktails)
API = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic"

# Detail-Endpunkt für Drink-Details
DETAIL_API = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i="

# Funktion: Alle Mocktails abrufen (zunächst IDs und Namen)
def get_mocktails():
    response = requests.get(API)
    if response.status_code == 200:
        try:
            return response.json()["drinks"]
        except requests.exceptions.JSONDecodeError:
            st.error("Fehler beim Verarbeiten der Antwort von der API.")
            return []
    else:
        st.error(f"Fehler beim Abrufen: Status-Code {response.status_code}")
        return []

# Detaildaten zu einem Drink holen
def get_drink_details(drink_id):
    response = requests.get(f"{DETAIL_API}{drink_id}")
    if response.status_code == 200:
        try:
            return response.json()["drinks"][0]
        except:
            return None
    return None

# Funktion: Rezept anzeigen & Daten für Favoriten vorbereiten
def display_recipe(drink):
    st.image(drink["strDrinkThumb"], width=300)
    st.markdown(f"### 🥂 {drink['strDrink']}")
    st.markdown(f"**Glas:** {drink['strGlass']}")
    st.markdown("#### 🧂 Zutaten:")

    zutaten_liste = []
    for i in range(1, 16):
        zutat = drink.get(f"strIngredient{i}")
        menge = drink.get(f"strMeasure{i}")
        if zutat:
            zutaten_liste.append({"name": zutat, "amount": menge if menge else ""})
            st.write(f"- {menge if menge else ''} {zutat}")

    anleitung = drink.get("strInstructionsDE") or drink.get("strInstructions") or "Keine Anleitung verfügbar."
    st.markdown("#### 📖 Zubereitung:")
    st.write(anleitung)

    return {
        "titel": drink["strDrink"],
        "beschreibung": {
            "ingredients": zutaten_liste,
            "instructions": [anleitung]
        }
    }

# Hauptfunktion
def main():
    st.title("🍹 Mocktail-Rezepte & Favoriten")

    # Session-State initialisieren
    if "favoriten" not in st.session_state:
        st.session_state["favoriten"] = []

    # Alle Mocktails abrufen
    mocktails = get_mocktails()

    # Eingabefeld zur Filterung
    cocktail_name = st.text_input("🔍 Filtere nach einem Mocktail-Namen:")

    # Gefilterte Mocktails
    gefilterte_mocktails = [m for m in mocktails if cocktail_name.lower() in m["strDrink"].lower()] if cocktail_name else mocktails

    if gefilterte_mocktails:
        for mocktail in gefilterte_mocktails:
            with st.expander(mocktail["strDrink"]):
                drink = get_drink_details(mocktail["idDrink"])
                if drink:
                    rezept_objekt = display_recipe(drink)

                    if st.button("⭐ Zu Favoriten hinzufügen", key=f"fav_{mocktail['idDrink']}"):
                        favoriten = st.session_state["favoriten"]
                        if not any(f["titel"] == rezept_objekt["titel"] for f in favoriten):
                            favoriten.append(rezept_objekt)
                            st.success(f"'{rezept_objekt['titel']}' wurde zu den Favoriten hinzugefügt!")
                        else:
                            st.warning(f"'{rezept_objekt['titel']}' ist bereits in den Favoriten.")
    else:
        st.error("❌ Kein Mocktail gefunden.")

    # Favoriten anzeigen
    if st.session_state["favoriten"]:
        st.markdown("---")
        st.markdown("## ⭐ Ihre Favoriten")
        for fav in st.session_state["favoriten"]:
            with st.expander(fav["titel"]):
                st.markdown("### 🧂 Zutaten:")
                for z in fav["beschreibung"]["ingredients"]:
                    st.write(f"- {z['amount']} {z['name']}")
                st.markdown("### 📖 Zubereitung:")
                for step in fav["beschreibung"]["instructions"]:
                    st.write(f"- {step}")

if __name__ == "__main__":
    main()
