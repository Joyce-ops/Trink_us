import streamlit as st
import json
from pathlib import Path

# ====== App Layout und Titel ======
st.set_page_config(page_title="Cocktail Creator", page_icon="🍹", layout="centered")

# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

st.title("🍸 Dein eigener Cocktail-Mixer")

# ====== Datei für gespeicherte Cocktails ======
SAVE_FILE = Path("cocktails.json")

# Funktion zum Laden gespeicherter Cocktails
def load_cocktails():
    if SAVE_FILE.exists():
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    return {}

# Funktion zum Speichern von Cocktails
def save_cocktails(cocktails):
    with open(SAVE_FILE, "w") as file:
        json.dump(cocktails, file)

# Gespeicherte Cocktails laden
cocktails = load_cocktails()

# ====== Cocktailname ======
cocktail_name = st.text_input("Gib deinem Cocktail einen Namen:")

# ====== Basis-Spirituose auswählen ======
base = st.selectbox("Wähle deine Basis-Spirituose:", [
    "Rum", "Wodka", "Gin", "Tequila", "Whiskey", "Likör", "Ohne Alkohol"
])

st.divider()

# ====== Zutaten-Auswahl ======
st.subheader("Zutaten auswählen oder eigene hinzufügen")

default_ingredients = [
    "Limettensaft", "Zitronensaft", "Orangensaft", "Ananassaft",
    "Cola", "Tonic Water", "Soda", "Zuckersirup",
    "Grenadine", "Minze", "Eiswürfel", "Ingwer", "Basilikum"
]

# Session State für benutzerdefinierte Zutaten
if "custom_ingredients" not in st.session_state:
    st.session_state.custom_ingredients = []

# Kombinierte Zutatenliste anzeigen
all_ingredients = default_ingredients + st.session_state.custom_ingredients
selected_ingredients = st.multiselect("Wähle deine Zutaten:", all_ingredients)

# ====== Eigene Zutat hinzufügen ======
with st.form("Eigene Zutat hinzufügen"):
    custom_input = st.text_input("Eigene Zutat:", placeholder="z. B. Lavendel, Matcha...")
    submitted = st.form_submit_button("➕ Hinzufügen")
    if submitted:
        if custom_input and custom_input not in st.session_state.custom_ingredients:
            st.session_state.custom_ingredients.append(custom_input)
            st.success(f"'{custom_input}' wurde hinzugefügt!")
        elif custom_input in st.session_state.custom_ingredients:
            st.warning("Diese Zutat wurde bereits hinzugefügt.")
        else:
            st.warning("Bitte gib eine gültige Zutat ein.")

st.divider()

# ====== Deko wählen ======
decoration = st.selectbox("Wähle eine Dekoration:", [
    "Limettenscheibe", "Cocktailkirsche", "Minzzweig", "Zuckerrand", "Keine"
])

# ====== Cocktail mixen Button ======
if st.button("🍹 Cocktail mixen!"):
    if not cocktail_name:
        st.warning("Bitte gib deinem Cocktail einen Namen.")
    else:
        # Cocktail speichern
        cocktails[cocktail_name] = {
            "Basis": base,
            "Zutaten": selected_ingredients,
            "Deko": decoration
        }
        save_cocktails(cocktails)
        st.success(f"**{cocktail_name}** ist fertig gemixt und wurde gespeichert!")
        st.markdown(f"""
        **Rezept für _{cocktail_name}_:**

        - **Basis:** {base}  
        - **Zutaten:** {', '.join(selected_ingredients) if selected_ingredients else 'Keine'}  
        - **Deko:** {decoration}
        """)

st.divider()

# ====== Gespeicherte Cocktails anzeigen ======
st.subheader("Gespeicherte Cocktails")
if cocktails:
    for name, details in cocktails.items():
        st.markdown(f"""
        **{name}**
        - **Basis:** {details['Basis']}
        - **Zutaten:** {', '.join(details['Zutaten']) if details['Zutaten'] else 'Keine'}
        - **Deko:** {details['Deko']}
        """)
else:
    st.info("Es wurden noch keine Cocktails gespeichert.")