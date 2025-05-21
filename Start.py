# ====== Start Init Block ======
# This needs to copied on top of the entry point of the app (Start.py)

import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import streamlit as st

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Trink_us")  # switch drive 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# load the data from the persistent storage into the session state
data_manager.load_user_data(
    session_state_key='fav_df', 
    file_name='favoriten.csv', 
    initial_value = pd.DataFrame(), 
    parse_dates = ['timestamp']
    )

# ====== End Init Block ======
# Theme-Funktion: Hell/Dunkel-Modus
# ==============================

def apply_theme():
    dark_mode = st.session_state.get("dark_mode", False)
    if dark_mode:
        image_url = "https://lamanne-paris.fr/wp-content/uploads/2021/07/astuces-ruiner-2048x1234.jpeg"
        overlay_color = "rgba(0, 0, 0, 0.7)"
        text_color = "#ffffff"
        box_bg_color = "rgba(0, 0, 0, 0.6)"
    else:
        image_url = "https://lamanne-paris.fr/wp-content/uploads/2021/07/astuces-ruiner-2048x1234.jpeg"
        overlay_color = "rgba(255, 255, 255, 0.5)"
        text_color = "#000000"
        box_bg_color = "rgba(255, 255, 255, 0.85)"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient({overlay_color}, {overlay_color}),
                        url("{image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }}

        .stApp > div:first-child {{
            background-color: {box_bg_color};
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}

        /* ALLE Textelemente robust ansprechen */
        [data-testid="stMarkdownContainer"],
        [data-testid="stHeader"],
        [data-testid="stText"],
        [data-testid="stTitle"],
        [data-testid="stSubheader"],
        [data-testid="stCaption"],
        [data-testid="stExpander"],
        [data-testid="stForm"],
        .stMarkdown, .stText, .stTitle, .stSubheader {{
            color: {text_color} !important;
        }}

        /* Info-Boxen */
        div[data-testid="stAlert"] {{
            background-color: rgba(255, 0, 0, 0.2) !important;
            border-left: none !important;
            color: {text_color} !important;
        }}

        /* Eingabefelder */
        input, textarea, select {{
            color: {text_color} !important;
        }}

        /* Tabellen */
        .stDataFrame, .stTable {{
            color: {text_color} !important;
        }}

        /* Button-Stil */
        .stButton > button {{
            color: {text_color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialisierung für Darkmode
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Toggle für Dunkelmodus in der Sidebar
st.sidebar.markdown("## Anzeige")
st.session_state["dark_mode"] = st.sidebar.toggle("🌙 Dunkelmodus", value=st.session_state["dark_mode"])

# Theme anwenden
apply_theme()


# ==============================
# Startseite Inhalt
# ==============================

# Initialisiere den Seitenstatus
if "page" not in st.session_state:
    st.session_state["page"] = "main"

# Titel der Seite
st.title('Cocktail Rezepte')

# Begrüßung des Benutzers
name = st.session_state.get('name', 'Gast')
st.markdown(f"✨ Hallo {name}! ✨")
st.markdown("Willkommen bei Trink us. Bei uns findest du zahlreiche Cocktails, die deinen Abend unvergesslich und geschmacksvoll machen. Für jeden Cocktail-Enthusiast ist etwas dabei!! 🍹")

# Hinweis zum Alkoholkonsum
st.info("""
##### **❗Hinweis zum Alkoholkonsum:❗**  
Diese Cocktailrezepte enthalten alkoholische Zutaten.  
Wenn du noch nicht volljährig bist, empfehlen wir dir, die Rezepte ohne Alkohol zuzubereiten als leckere Mocktail-Variante!  
Genieße verantwortungsvoll und altersgerecht. 🍸✨
""")

# Entwicklerhinweis
st.write("Diese App wurde von Carmen Hurschler, Mcqulat Miller und Joyce Baumann im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")
