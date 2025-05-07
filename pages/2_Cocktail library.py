import requests
import streamlit as st

API = "https://www.thecocktaildb.com/api"

def get_cocktails(cocktail_name=None):
    api_url = f"{API}/json/v1/1/search.php?s={cocktail_name}"
    response = requests.get(api_url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except requests.exceptions.JSONDecodeError:
            st.error("Ungültige Antwort von der API. JSON konnte nicht dekodiert werden.")
            return None
    else:
        st.error(f"Fehler beim Abrufen der Daten. Status-Code: {response.status_code}")
        return None

def display_recipe(drink):
    st.image(drink["strDrinkThumb"], width=300)
    st.markdown(f"### 🥂 {drink['strDrink']}")
    st.markdown(f"**Glasempfehlung:** {drink['strGlass']}")
    st.markdown("#### 🧂 Zutaten:")
    for i in range(1, 16):
        zutat = drink.get(f"strIngredient{i}")
        menge = drink.get(f"strMeasure{i}")
        if zutat:
            st.write(f"- {menge if menge else ''} {zutat}")
    st.markdown("#### 📖 Zubereitung:")
    st.write(drink["strInstructionsDE"] or drink["strInstructions"] or "Keine Anleitung verfügbar.")

def main():
    st.set_page_config(page_title="Cocktail-Rezepte", page_icon="🍹")
    st.title("🍸 Cocktail library")
    cocktail_name = st.text_input("Gib einen Cocktailnamen ein (z. B. Margarita, Mojito, Daiquiri):")

    # Favoriten initialisieren
    if "favoriten" not in st.session_state:
        st.session_state["favoriten"] = []

    # Rezept anzeigen
    if st.button("Rezept anzeigen"):
        if cocktail_name:
            daten = get_cocktails(cocktail_name)
            if daten and daten["drinks"]:
                for drink in daten["drinks"]:
                    with st.expander(drink["strDrink"]):
                        display_recipe(drink)
                        # Favorit hinzufügen
                        if st.button(f"Zu Favoriten hinzufügen: {drink['strDrink']}", key=f"fav_{drink['idDrink']}"):
                            # Favoriten aktualisieren
                            favoriten = st.session_state.get("favoriten", [])
                            if drink["strDrink"] not in favoriten:
                                favoriten.append(drink["strDrink"])
                                st.session_state["favoriten"] = favoriten
                                st.success(f"'{drink['strDrink']}' wurde zu den Favoriten hinzugefügt!")
                            else:
                                st.warning(f"'{drink['strDrink']}' ist bereits in den Favoriten.")
            else:
                st.error("Kein Cocktail mit diesem Namen gefunden.")
        else:
            st.warning("Bitte gib einen Namen ein.")

    # Favoriten anzeigen
    st.markdown("## 🌟 Deine Favoriten")
    if st.session_state["favoriten"]:
        for fav in st.session_state["favoriten"]:
            st.write(f"- {fav}")
    else:
        st.write("Noch keine Favoriten gespeichert.")

if __name__ == "__main__":
    main()