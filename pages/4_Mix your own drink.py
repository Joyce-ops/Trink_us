import streamlit as st
import json
from pathlib import Path
from utils.theme import apply_theme

# ====== App Layout und Titel ======
st.set_page_config(page_title="Cocktail Creator", page_icon="🍹", layout="centered")

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Theme anwenden
apply_theme()

# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

# ====== Hintergrundbild und Box-Design für beide Modi ======
image_url = "https://www.azuniatequila.com/wp-content/uploads/2020/01/Bar-Tools-Set-1024x713.jpg"
if st.session_state["dark_mode"]:
    # Dark Mode: Bild mit dunklem Overlay
    bg_style = f"""
        background: linear-gradient(rgba(20,20,20,0.85), rgba(20,20,20,0.85)), url("{image_url}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    """
    main_bg = "rgba(30,30,30,0.85)"  # dunkler Bereich im Dark Mode
    border = "#222"
else:
    # Light Mode: Bild ohne Overlay
    bg_style = f"""
        background: url("{image_url}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    """
    main_bg = "rgba(255,255,255,0.85)"  # weißer Bereich im Light Mode
    border = "#fff"

st.markdown(
    f"""
    <style>
    .stApp {{
        {bg_style}
    }}
    .main > div {{
        background-color: {main_bg};
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
        border: 2px solid {border};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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

default_ingredients = [
    "Limettensaft", "Zitronensaft", "Orangensaft", "Ananassaft", "Salz",
    "Zucker", "Agavendicksaft", "Zitronenlimonade", "Tonic Water", "Sprite",
    "Bitter Lemon", "Grenadine", "Himbeersirup", "Kokosnusscreme", "Kokosmilch",
    "Erdbeeren", "Himbeeren", "Blaubeeren", "Ananas", "Mango", "Kiwi", "Banane",
    "Pfirsich", "Melone", "Trauben", "Kirschen", "Zimt", "Vanille", "Ingwer",   
    "Cola", "Soda", "Zuckersirup", "Minze", "Basilikum", "Rosmarin", "Thymian",
    "Pfeffer", "Chili", "Lavendel", "Matcha", "Kardamom", "Muskatnuss", 
    "Koriander", "Anis", "Nelken", "Pfefferminzsirup", "Eiswürfel"   
]

# Kombinierte Zutatenliste anzeigen
all_ingredients = default_ingredients + st.session_state.get("custom_ingredients", [])
selected_ingredients = st.multiselect("Wähle deine Zutaten:", all_ingredients)

# ====== Deko wählen ======
decoration = st.selectbox("Wähle eine Dekoration:", [
    "Limettenscheibe", "Cocktailkirsche",  "Minzzweig", "Zuckerrand", "Keine"
])

# ====== Cocktail mixen Button ======
if st.button("🍹 Cocktail mixen!"):
    if not cocktail_name:
        st.warning("Bitte gib deinem Cocktail einen Namen.")
    else:
        if not selected_ingredients:
            st.warning("Bitte wähle mindestens eine Zutat aus.")
        else:
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
            - **Zutaten:** {', '.join(selected_ingredients)}  
            - **Deko:** {decoration}
            """)

st.divider()

# ====== Gespeicherte Cocktails anzeigen ======
st.subheader("Gespeicherte Cocktails")
if cocktails:
    for name, details in cocktails.items():
        st.markdown(f"""
        ### {name} 
        - **Basis:** {details['Basis']}
        - **Zutaten:** {', '.join(details['Zutaten']) if details['Zutaten'] else 'Keine'}
        - **Deko:** {details['Deko']}
        """)
else:
    st.info("Es wurden noch keine Cocktails gespeichert.")