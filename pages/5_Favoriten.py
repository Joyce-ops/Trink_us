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
st.title("Ihre Favoriten 🍹")

# Sicherstellen, dass die Favoriten-Daten vorhanden sind
if "fav_df" in st.session_state and not st.session_state.fav_df.empty:
    df = st.session_state.fav_df.copy()

    if "Suchbegriff" in df.columns:
        # Filter und Duplikate entfernen
        suchbegriffe_df = (
            df[["Suchbegriff"]]
            .dropna(subset=["Suchbegriff"])
            .query("Suchbegriff != 'none' and Suchbegriff != ''")
            .drop_duplicates()
            .sort_values("Suchbegriff")
            .reset_index(drop=True)
        )

        
        st.dataframe(suchbegriffe_df, use_container_width=True)

        # Auswahl der zu löschenden Suchbegriffe
        to_delete = st.multiselect(
            "Drink zum Löschen auswählen:",
            options=suchbegriffe_df["Suchbegriff"].tolist()
        )

        if st.button("Ausgewählten Drink löschen"):
            if to_delete:
                # Filtere alle Zeilen aus fav_df raus, deren Suchbegriff in to_delete ist
                new_df = df[~df["Suchbegriff"].isin(to_delete)].reset_index(drop=True)
                st.session_state.fav_df = new_df  # Update im session_state

                st.success(f"{len(to_delete)} Drink(s) wurden gelöscht.")
                st.experimental_rerun()  # Seite neu laden, damit Tabelle aktualisiert wird
            else:
                st.warning("Bitte mindestens einen Drink zum Löschen auswählen.")
    else:
        st.warning("Die Spalte 'Suchbegriff' wurde nicht gefunden.")
else:
    st.info("Keine Favoriten gefunden.")
