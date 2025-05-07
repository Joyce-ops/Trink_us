import os
import streamlit as st
from PIL import Image
import json
import pandas as pd  # Für das Lesen der CSV-Datei


# Pfad zum drinks-Ordner und zur CSV-Datei
pages_folder = os.path.dirname(os.path.abspath(__file__))
drinks_folder = os.path.join(pages_folder, "../drinks")
csv_path = os.path.join(drinks_folder, "drinks.csv")

# Überschrift der Seite
st.title("Übersicht Cocktail Klassiker")

# Überprüfen, ob die CSV-Datei existiert
if os.path.exists(csv_path):
    # CSV-Datei laden
    drinks_df = pd.read_csv(csv_path)

    # Spalten für die Darstellung (3 Spalten)
    columns = st.columns(3)  # Drei Spalten erstellen
    col_index = 0  # Startindex für die Spalten
    
    # Für jeden Drink in der CSV-Datei
    for _, row in drinks_df.iterrows():
        drink_name = row["name"]
        drink_folder = os.path.join(drinks_folder, drink_name)
        
        # Überprüfen, ob der Ordner für den Drink existiert
        if os.path.exists(drink_folder):
            # Inhalt in der aktuellen Spalte anzeigen
            with columns[col_index]:
                # Bild anzeigen
                st.subheader(drink_name)
                image_path = os.path.join(drink_folder, "image.jpg")
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    st.image(image, caption=drink_name, width=150)
                else:
                    st.warning(f"Kein Bild für {drink_name} gefunden.")
                
                # Button für das Rezept
                if st.button(f"Rezept {drink_name}", key=f"rezept_{drink_name}"):
                    # JSON-Rezeptdatei lesen
                    recipe_path = os.path.join(drink_folder, "rezept.json")
                    if os.path.exists(recipe_path):
                        with open(recipe_path, "r", encoding="utf-8") as file:
                            recipe_content = json.load(file)
                        
                        # Rezeptdetails anzeigen
                        st.write("### Zutaten:")
                        for ingredient in recipe_content.get("ingredients", []):
                            name, amount = ingredient.get("name"), ingredient.get("amount")
                            if name and amount:
                                st.write(f"- {amount} {name}")
                            else:
                                st.write("- Unbekannte Zutat")
                        
                        st.write("### Zubereitung:")
                        st.write(recipe_content.get("instructions", "Keine Anweisungen verfügbar."))
                    else:
                        st.warning(f"Kein Rezept für {drink_name} gefunden: {recipe_path}")
        
        # Zum nächsten Drink in die nächste Spalte wechseln
        col_index = (col_index + 1) % 3  # Zyklisch zwischen 0, 1 und 2 wechseln
else:
    st.error("Die Datei 'drinks.csv' wurde nicht gefunden!")