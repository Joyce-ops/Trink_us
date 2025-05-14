import os
import json
import requests
import streamlit as st

# Titel der Seite
st.title("🍹 Cocktail Library")

# Pfad zur JSON-Datei für Favoriten
pages_folder = os.path.dirname(os.path.abspath(__file__))
favoriten_datei = os.path.join(pages_folder, "../favoriten.json")

# Favoriten aus der JSON-Datei laden
def favoriten_laden():
    if os.path.exists(favoriten_datei):
        with open(favoriten_datei, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                st.error("Fehler beim Laden der Favoriten. Die Datei ist beschädigt.")
                return []
    return []

# Favoriten in der JSON-Datei speichern
def favoriten_speichern(favoriten):
    with open(favoriten_datei, "w", encoding="utf-8") as file:
        json.dump(favoriten, file, ensure_ascii=False, indent=4)

# Favoriten initialisieren
favoriten = favoriten_laden()

# Validierung der Favoriten-Liste
favoriten = [fav for fav in favoriten if "idDrink" in fav]

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

# Suchleiste für Cocktails
suchbegriff = st.text_input("🔍 Suche nach einem Cocktail:", placeholder="Gib einen Cocktailnamen ein...")

# Cocktails suchen und anzeigen
if suchbegriff:
    cocktails = suche_cocktails(suchbegriff)
    if cocktails:
        for cocktail in cocktails:
            st.image(cocktail["strDrinkThumb"], width=150)
            st.write(f"### {cocktail['strDrink']}")
            
            # Button zum Hinzufügen zu Favoriten
            if st.button(f"Zu Favoriten hinzufügen: {cocktail['strDrink']}", key=f"add_fav_{cocktail['idDrink']}"):
                # Überprüfen, ob der Cocktail bereits in den Favoriten ist
                if not any(fav.get("idDrink") == cocktail["idDrink"] for fav in favoriten):
                    # Favorit hinzufügen
                    favoriten.append(cocktail)
                    favoriten_speichern(favoriten)  # Favoriten speichern
                    st.success(f"'{cocktail['strDrink']}' wurde zu den Favoriten hinzugefügt!")
                else:
                    st.warning(f"'{cocktail['strDrink']}' ist bereits in den Favoriten.")
    else:
        st.warning("Keine Cocktails gefunden. Bitte versuche es mit einem anderen Suchbegriff.")
else:
    st.info("Gib einen Suchbegriff ein, um Cocktails zu finden.")