import os
import streamlit as st
from PIL import Image
import json  # JSON-Modul importieren

# Pfad zum Ordner mit den Rezepten
drinks_folder = "./drinks"

# Überschrift der Seite
st.title("Übersicht Cocktail Klassiker")

# Überprüfen, ob der Ordner existiert
if os.path.exists(drinks_folder):
    # Alle Dateien im Ordner auflisten
    for drink_file in os.listdir(drinks_folder):
        # Pfad zur Datei
        drink_path = os.path.join(drinks_folder, drink_file)
        
        # Überprüfen, ob es ein Ordner ist (für jedes Rezept)
        if os.path.isdir(drink_path):
            # Name des Rezepts (Ordnername)
            drink_name = os.path.basename(drink_path)
            
            # Bildpfad (angenommen, das Bild heißt "image.jpg" im Rezeptordner)
            image_path = os.path.join(drink_path, "image.jpg")
            
            # Rezept anzeigen
            st.subheader(drink_name)
            
            # Bild anzeigen, falls vorhanden
            if os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, caption=drink_name, use_column_width=True)
            
            # JSON-Rezeptdatei lesen
            recipe_path = os.path.join(drink_path, "recipe.json")
            if os.path.exists(recipe_path):
                with open(recipe_path, "r", encoding="utf-8") as file:
                    recipe_content = json.load(file)  # JSON-Inhalt laden
                
                # Rezeptdetails anzeigen
                st.write("### Zutaten:")
                for ingredient in recipe_content.get("ingredients", []):
                    st.write(f"- {ingredient}")
                
                st.write("### Zubereitung:")
                st.write(recipe_content.get("instructions", "Keine Anweisungen verfügbar."))
else:
    st.error("Der Ordner 'drinks' wurde nicht gefunden.")