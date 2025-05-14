import os
import json
import requests
import streamlit as st

# Titel der Seite
st.title("🍹 Mocktail Library")

# Zusätzlicher Zeilenumbruch, um die Darstellung weiter unten zu starten
st.markdown("<br>", unsafe_allow_html=True)

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

# Funktion: Details eines Mocktails abrufen
def mocktail_details(mocktail_id):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={mocktail_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("drinks", [])[0]  # Gib das erste Ergebnis zurück
    else:
        st.error("Fehler beim Abrufen der Mocktail-Details. Bitte versuche es später erneut.")
        return None

# CSS für größere Mocktail-Namen und zentrierte Rezepttexte
st.markdown(
    """
    <style>
    div[data-testid="stButton"] > button {
        font-size: 12px; /* Kleinere Schriftgröße für Buttons */
    }
    .mocktail-name {
        font-size: 22px; /* Größere Schriftgröße für Mocktail-Namen */
        margin-top: 5px;
        margin-bottom: 5px;
        text-align: center;
        font-weight: bold;
    }
    .recipe-text {
        font-size: 14px; /* Einheitliche Schriftgröße für Rezepttexte */
        margin-top: 5px;
        margin-bottom: 5px;
        text-align: center; /* Zentrierte Texte */
    }
    .stTextInput > div > div:first-child {
        margin-bottom: 0px; /* Entfernt den Abstand zwischen Titel und Suchleiste */
    }
    .recipe-spacing {
        margin-top: 20px; /* Abstand zwischen Bild und Rezept */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Suchleiste für Mocktails
st.markdown('<label class="search-label">🔍 Suche nach einem Mocktail:</label>', unsafe_allow_html=True)
suchbegriff = st.text_input("", placeholder="Gib einen Mocktailnamen ein...")

# Mocktails suchen und anzeigen
mocktails = suche_mocktails(suchbegriff)  # Suche mit oder ohne Suchbegriff
if mocktails:
    # Titel über den Mocktails
    st.subheader("Mocktail Vorschläge ✨")

    # Tabelle für die Mocktail-Vorschläge
    for idx, mocktail in enumerate(mocktails):
        col1, col2, col3 = st.columns([1, 3, 3])  # Spaltenbreiten anpassen

        with col1:
            st.image(mocktail["strDrinkThumb"], width=100)  # Bild in der ersten Spalte

        with col2:
            st.markdown(f"<p class='mocktail-name'>{mocktail['strDrink']}</p>", unsafe_allow_html=True)

        with col3:
            if st.button("Rezept anzeigen", key=f"details_{mocktail['idDrink']}"):
                details = mocktail_details(mocktail["idDrink"])
                if details:
                    # Rezept in der zweiten Spalte anzeigen
                    with col2:
                        st.markdown("<div class='recipe-spacing'></div>", unsafe_allow_html=True)  # Abstand einfügen
                        st.markdown("<p class='recipe-text'><b>Zutaten:</b></p>", unsafe_allow_html=True)
                        for i in range(1, 16):  # Es gibt bis zu 15 Zutaten in der API
                            ingredient = details.get(f"strIngredient{i}")
                            measure = details.get(f"strMeasure{i}")
                            if ingredient:
                                st.markdown(f"<p class='recipe-text'>- {measure or ''} {ingredient}</p>", unsafe_allow_html=True)
                        st.markdown("<p class='recipe-text'><b>Zubereitung:</b></p>", unsafe_allow_html=True)
                        st.markdown(f"<p class='recipe-text'>{details.get('strInstructions', 'Keine Zubereitungsanweisungen verfügbar.')}</p>", unsafe_allow_html=True)
            if st.button("Zu Favoriten hinzufügen", key=f"add_fav_{mocktail['idDrink']}"):
                if not any(fav.get("idDrink") == mocktail["idDrink"] for fav in favoriten):
                    favoriten.append(mocktail)
                    favoriten_speichern(favoriten)
                    st.success(f"'{mocktail['strDrink']}' wurde zu den Favoriten hinzugefügt!")
                else:
                    st.warning(f"'{mocktail['strDrink']}' ist bereits in den Favoriten.")
        
        # Horizontale Linie nach jedem Drink
        st.markdown("---")
else:
    st.warning("Keine Mocktails gefunden. Bitte versuche es mit einem anderen Suchbegriff.")