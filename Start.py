# ====== Start Init Block ======
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import streamlit as st
from utils.theme import apply_theme

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
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

st.sidebar.markdown("## Anzeige")
st.session_state["dark_mode"] = st.sidebar.toggle("🌙 Dunkelmodus", value=st.session_state["dark_mode"])

# Theme anwenden (NUR aus theme.py!)
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

