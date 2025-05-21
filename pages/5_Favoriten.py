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

if "fav_df" in st.session_state and not st.session_state.fav_df.empty:
    df = st.session_state.fav_df.copy()

    if "Suchbegriff" in df.columns:
        suchbegriffe_df = (
            df[["Suchbegriff"]]
            .dropna(subset=["Suchbegriff"])
            .query("Suchbegriff != 'none' and Suchbegriff != ''")
            .drop_duplicates()
            .sort_values("Suchbegriff")
            .reset_index(drop=True)
        )

        st.subheader("Suchbegriffe bearbeiten oder löschen")

        edited_df = st.experimental_data_editor(
            suchbegriffe_df,
            num_rows="dynamic",  # erlaubt Löschen von Zeilen
            key="suchbegriff_editor"
        )

        # Wenn Zeilen gelöscht oder geändert wurden, update die fav_df entsprechend
        if not edited_df.equals(suchbegriffe_df):
            # gefilterte Suchbegriffe, die noch in der bearbeiteten Tabelle sind
            verbleibende_begriffe = set(edited_df["Suchbegriff"].dropna().str.strip())

            # Update st.session_state.fav_df: nur Reihen behalten, deren Suchbegriff noch vorhanden ist
            new_df = df[df["Suchbegriff"].isin(verbleibende_begriffe)].reset_index(drop=True)
            st.session_state.fav_df = new_df

            st.success("Favoritenliste wurde aktualisiert!")

        st.dataframe(edited_df, use_container_width=True)

    else:
        st.warning("Die Spalte 'Suchbegriff' wurde nicht gefunden.")
else:
    st.info("Keine Favoriten gefunden.")
