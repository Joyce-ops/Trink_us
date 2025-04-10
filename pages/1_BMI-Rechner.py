# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

# ------------------------------------------------------------
# Here starts the actual app, which was developed previously
import streamlit as st
from functions.bmi_calculator import calculate_bmi

st.title('BMI Rechner')

with st.form("BMI Eingabeformular"):
    # Get user input for height and weight
    height = st.number_input('Geben Sie Ihre Größe ein (in Meter)', min_value=0.1, max_value=3.0, value=1.7, step=0.01)
    weight = st.number_input('Geben Sie Ihr Gewicht ein (in kg)', min_value=1.0, max_value=500.0, value=70.0, step=0.1)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    
if submitted:
    result = calculate_bmi(height, weight)
    st.write(f'Ihr BMI ist: {result["bmi"]}')
    st.write(f'Berechnet am: {result["timestamp"].strftime("%d.%m.%Y %H:%M:%S")}')
    st.write(f'Kategorie: {result["category"]}')
        
    # --- Save BMI data ---
    from utils.data_manager import DataManager
    DataManager().append_record(session_state_key='data_df', record_dict=result)  # update data in session state and storage


        

        