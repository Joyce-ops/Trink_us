import requests
import streamlit as st

# Streamlit-Seitenkonfiguration muss zuerst kommen
st.set_page_config(page_title="Cocktail-Rezepte", page_icon="🍹")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

# API-URL
API = "https://www.thecocktaildb.com/api"

# Funktion: Cocktails suchen
def get_cocktails(cocktail_name=None):
    api_url = f"{API}/json/v1/1/search.php?s={cocktail_name}"
    response = requests.get(api_url)
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Fehler beim Verarbeiten der Antwort von der API.")
            return None
    else:
        st.error(f"Fehler beim Abrufen: Status-Code {response.status_code}")
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
    st.title("🍸 Cocktail-Rezepte & Favoriten")

    # Session-State initialisieren
    if "favoriten" not in st.session_state:
        st.session_state["favoriten"] = []

    # Eingabefeld für Cocktailsuche
    cocktail_name = st.text_input("🔍 Gib einen Cocktailnamen ein:")

    # Rezepte anzeigen
    if st.button("Rezepte suchen"):
        if cocktail_name:
            daten = get_cocktails(cocktail_name)
            if daten and daten["drinks"]:
                for drink in daten["drinks"]:
                    with st.expander(drink["strDrink"]):
                        rezept_objekt = display_recipe(drink)

                        # Eindeutiger Button pro Rezept
                        if st.button("⭐ Zu Favoriten hinzufügen", key=f"fav_{drink['idDrink']}"):
                            favoriten = st.session_state["favoriten"]
                            # Duplikate verhindern
                            if not any(f["titel"] == rezept_objekt["titel"] for f in favoriten):
                                favoriten.append(rezept_objekt)
                                st.success(f"'{rezept_objekt['titel']}' wurde zu den Favoriten hinzugefügt!")
                            else:
                                st.warning(f"'{rezept_objekt['titel']}' ist bereits in den Favoriten.")
            else:
                st.error("❌ Kein Cocktail gefunden.")
        else:
            st.warning("Bitte gib einen Namen ein.")

    # Favoriten anzeigen
    if st.session_state["favoriten"]:
        st.markdown("---")
        st.markdown("## ⭐ Ihre Favoriten")
        for index, fav in enumerate(st.session_state["favoriten"]):
            with st.expander(fav["titel"]):
                st.markdown("### 🧂 Zutaten:")
                for z in fav["beschreibung"]["ingredients"]:
                    st.write(f"- {z['amount']} {z['name']}")
                st.markdown("### 📖 Zubereitung:")
                for step in fav["beschreibung"]["instructions"]:
                    st.write(f"- {step}")

if __name__ == "__main__":
    main()