# ====== Start Init Block ======
# This needs to copied on top of the entry point of the app (Start.py)

import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Trink_us")  # switch drive 

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

st.title('Cocktail Rezepte')

name = st.session_state.get('name')
st.markdown(f"✨ Hallo {name}! ✨")
st.markdown("Hier finden Sie Rezepte zu Klassieschen Cocktails. Für jeden Cocktail-Enthiusiast ist etwas dabei!! 🍹🍸")
        
# Add some  advice
st.info("""Diese Cocktail Rezepte enthalten Alkohol, falls Sie nicht volljährig sind, sind diese Rezepte nicht für Sie geeignet. 
Bitte machen sie die Rezepte ohne den Alkohol.""")

st.write("Diese App wurde von Carmen Hurschler, Mcqulat Miller und Joyce Baumann im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")