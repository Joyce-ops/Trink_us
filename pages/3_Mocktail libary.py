import os
import json
import requests
import streamlit as st

# Funktion: CSS für einen weich überlagerten und dunkleren Hintergrund
def set_faded_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), /* Dunkler Overlay */
                        url("{image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }}

        .main > div {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}

        /* Stil für die Suchleiste */
        .search-label {{
            color: #333333; /* Dunklere Schriftfarbe */
            font-size: 1.1rem; /* Leicht größere Schriftgröße */
            font-weight: 500; /* Leicht dickere Schrift */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Dein aktuelles Hintergrundbild (Mocktails)
image_url = "https://img.freepik.com/premium-photo/selection-colorful-mocktails_941600-17041.jpg"

# Hintergrund anwenden
set_faded_background(image_url)

# Titel der Seite
st.title("🍹 Mocktail Library")

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

# Funktion: Mocktails aus der API suchen
def suche_mocktails(suchbegriff=None):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        drinks = data.get("drinks", [])
        if suchbegriff:
            # Filtere die Mocktails basierend auf dem Suchbegriff
            return [drink for drink in drinks if suchbegriff.lower() in drink["strDrink"].lower()]
        return drinks  # Zeige alle Mocktails, wenn kein Suchbegriff eingegeben wurde
    else:
        st.error("Fehler beim Abrufen der Mocktails. Bitte versuche es später erneut.")
        return []

# Suchleiste für Mocktails
st.markdown('<label class="search-label">🔍 Suche nach einem Mocktail:</label>', unsafe_allow_html=True)
suchbegriff = st.text_input("", placeholder="Gib einen Mocktailnamen ein...")

# Mocktails suchen und anzeigen
mocktails = suche_mocktails(suchbegriff)  # Suche mit oder ohne Suchbegriff
if mocktails:
    for mocktail in mocktails:
        st.image(mocktail["strDrinkThumb"], width=150)
        st.write(f"### {mocktail['strDrink']}")
        
        # Button zum Hinzufügen zu Favoriten
        if st.button(f"Zu Favoriten hinzufügen: {mocktail['strDrink']}", key=f"add_fav_{mocktail['idDrink']}"):
            # Überprüfen, ob der Mocktail bereits in den Favoriten ist
            if not any(fav.get("idDrink") == mocktail["idDrink"] for fav in favoriten):
                # Favorit hinzufügen
                favoriten.append(mocktail)
                favoriten_speichern(favoriten)  # Favoriten speichern
                st.success(f"'{mocktail['strDrink']}' wurde zu den Favoriten hinzugefügt!")
            else:
                st.warning(f"'{mocktail['strDrink']}' ist bereits in den Favoriten.")
else:
    st.warning("Keine Mocktails gefunden. Bitte versuche es mit einem anderen Suchbegriff.")