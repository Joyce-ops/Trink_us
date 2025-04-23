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
    
    # Für jeden Drink in der CSV-Datei
    for _, row in drinks_df.iterrows():
        drink_name = row["name"]
        drink_folder = os.path.join(drinks_folder, drink_name)
        
        # Überprüfen, ob der Ordner für den Drink existiert
        if os.path.exists(drink_folder):
            st.subheader(drink_name)
            
            # Bildpfad
            image_path = os.path.join(drink_folder, "image.jpg")
            if os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, caption=drink_name, use_column_width=True)
            else:
                st.warning(f"Kein Bild für {drink_name} gefunden.")
            
            # JSON-Rezeptdatei lesen
            recipe_path = os.path.join(drink_folder, "recipe.json")
            if os.path.exists(recipe_path):
                with open(recipe_path, "r", encoding="utf-8") as file:
                    recipe_content = json.load(file)
                
                # Rezeptdetails anzeigen
                st.write("### Zutaten:")
                for ingredient in recipe_content.get("ingredients", []):
                    st.write(f"- {ingredient}")
                
                st.write("### Zubereitung:")
                st.write(recipe_content.get("instructions", "Keine Anweisungen verfügbar."))
            else:
                st.warning(f"Kein Rezept für {drink_name} gefunden.")
        else:
            st.error(f"Der Ordner für {drink_name} wurde nicht gefunden.")
else:
    st.error("Die Datei 'drinks.csv' wurde nicht gefunden!")
