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
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value=pd.DataFrame(), 
    parse_dates=['timestamp']
)
# ====== End Init Block ======

# ------------------------------------------------------------
# Here starts the actual app, which was developed previously

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