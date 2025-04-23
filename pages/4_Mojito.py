import os
import streamlit as st
from PIL import Image
import json  # JSON-Modul importieren

# Pfad zum Ordner mit den Rezepten (drinks-Ordner)
pages_folder = os.path.dirname(os.path.abspath(__file__))
drinks_folder = os.path.join(pages_folder, "../drinks")  # drinks-Ordner relativ zum pages-Ordner
mojito_folder = os.path.join(drinks_folder, "Mojito")

# Überschrift der Seite
st.title("Übersicht Cocktail Klassiker")

# Button für Mojito hinzufügen
if st.button("Zeige Mojito-Rezept"):
    if os.path.exists(mojito_folder):
        # Bildpfad
        image_path = os.path.join(mojito_folder, "image.jpg")
        if os.path.exists(image_path):
            image = Image.open(image_path)
            st.image(image, caption="Mojito", use_column_width=True)
        else:
            st.warning("Das Bild für Mojito wurde nicht gefunden.")
        
        # JSON-Rezeptdatei lesen
        rezept_path = os.path.join(mojito_folder, "rezept.json")
        if os.path.exists(rezept_path):
            with open(rezept_path, "r", encoding="utf-8") as file:
                rezept_content = json.load(file)  # JSON-Inhalt laden
            
            # Rezeptdetails anzeigen
            st.write("### Zutaten:")
            for ingredient in rezept_content.get("ingredients", []):
                st.write(f"- {ingredient}")
            
            st.write("### Zubereitung:")
            st.write(rezept_content.get("instructions", "Keine Anweisungen verfügbar."))
        else:
            st.warning("Die Rezeptdatei für Mojito wurde nicht gefunden.")
    else:
        st.error("Der Mojito-Ordner wurde nicht gefunden.")