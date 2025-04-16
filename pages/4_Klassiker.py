import os
import streamlit as st
from PIL import Image

# Pfad zum Ordner mit den Rezepten
drinks_folder = "./drinks"

# Überschrift der Seite
st.title("Klassiker Übersicht")

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
            
            # Link zur Rezeptdatei (angenommen, es gibt eine Datei "recipe.txt")
            recipe_path = os.path.join(drink_path, "recipe.txt")
            if os.path.exists(recipe_path):
                with open(recipe_path, "r", encoding="utf-8") as file:
                    recipe_content = file.read()
                if st.button(f"Rezept anzeigen: {drink_name}"):
                    st.text(recipe_content)
else:
    st.error("Der Ordner 'drinks' wurde nicht gefunden.")