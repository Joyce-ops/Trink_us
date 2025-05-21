# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('favoriten.py')
# ====== End Login Block ======

import streamlit as st
import pandas as pd
from utils.theme import apply_theme

# Theme
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
apply_theme()

# Login prüfen
username = st.session_state.get("username")
if not username:
    st.error("Bitte zuerst einloggen!")
    st.stop()

# Titel
st.title("🔍 Ihre Suchbegriffe")

# Beispiel-Datenstruktur: search_df mit Timestamp und Suchbegriff
# Diese muss an anderer Stelle mit neuen Einträgen befüllt werden
if "search_df" in st.session_state and not st.session_state.search_df.empty:
    df = st.session_state.search_df.copy()

    # timestamp als datetime, falls nötig
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Duplikate nach suchbegriff entfernen – nur der neueste bleibt
    df = df.sort_values("timestamp", ascending=False).drop_duplicates(subset=["suchbegriff"])

    # Optional: nach Zeit sortieren
    df = df.sort_values("timestamp", ascending=False)

    # Nur die Spalten zeigen, die gewünscht sind
    st.dataframe(df[["timestamp", "suchbegriff"]], use_container_width=True)
else:
    st.info("Noch keine Suchbegriffe vorhanden.")

from datetime import datetime

suchbegriff = st.text_input("Suchbegriff eingeben")
if suchbegriff:
    new_entry = pd.DataFrame([{
        "timestamp": datetime.now(),
        "suchbegriff": suchbegriff.strip()
    }])

    if "search_df" not in st.session_state:
        st.session_state.search_df = new_entry
    else:
        st.session_state.search_df = pd.concat([st.session_state.search_df, new_entry], ignore_index=True)




