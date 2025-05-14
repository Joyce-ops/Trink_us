# ====== Start Init Block ======
# This needs to copied on top of the entry point of the app (Start.py)

import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

import streamlit as st

# CSS-Funktion für blassen Hintergrund und Textanpassung
def set_faded_background_and_text(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)),
                        url("{image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }}

        /* Optional: Inhalte leicht hervorheben */
        .stApp > div:first-child {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}

        /* Text dunkler und leicht dicker */
        .stMarkdown, .stTitle, .stInfo {{
            color: #333333; /* Dunklere Schriftfarbe */
            font-weight: 500; /* Leicht dickere Schrift */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Deine Bild-URL
image_url = "https://lamanne-paris.fr/wp-content/uploads/2021/07/astuces-ruiner-2048x1234.jpeg"

# Hintergrund und Textanpassung anwenden
set_faded_background_and_text(image_url)

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="AppV1")  # switch drive 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# load the data from the persistent storage into the session state
data_manager.load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    parse_dates = ['timestamp']
    )
# ====== End Init Block ======

# ------------------------------------------------------------
# Here starts the actual app, which was developed previously
import streamlit as st

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
##### **ℹ️ Hinweis zum Alkoholkonsum: ℹ️**  
Diese Cocktailrezepte enthalten alkoholische Zutaten.  
Wenn du noch nicht volljährig bist, empfehlen wir dir, die Rezepte ohne Alkohol zuzubereiten als leckere Mocktail-Variante!  
Genieße verantwortungsvoll und altersgerecht. 🍸✨
""")

# Entwicklerhinweis
st.write("Diese App wurde von Carmen Hurschler, Mcqulat Miller und Joyce Baumann im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")