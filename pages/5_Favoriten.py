# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
from utils.theme import apply_theme
from utils.favoriten import favoriten_laden, favoriten_speichern

# Zustand für dark_mode sicherstellen
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

apply_theme()

st.title("Ihre Favoriten 🍹")

username = st.session_state.get("username")
favoriten = favoriten_laden(username)

if not favoriten:
    st.info("Noch keine Favoriten gespeichert.")
    st.stop()

# Favoriten löschen
st.markdown("### Favoriten verwalten")
favoriten_ids = [f"{f['idDrink']} - {f['strDrink']}" for f in favoriten]
auswahl = st.multiselect("Favoriten zum Löschen auswählen:", favoriten_ids)

if st.button("Ausgewählte löschen"):
    favoriten = [f for f in favoriten if f"{f['idDrink']} - {f['strDrink']}" not in auswahl]
    favoriten_speichern(username, favoriten)
    st.success("Ausgewählte Favoriten wurden gelöscht.")
    st.experimental_rerun()

# CSV-Export
csv_download = pd.DataFrame(favoriten).to_csv(index=False).encode("utf-8")
st.download_button(
    label="📤 Favoriten als CSV herunterladen",
    data=csv_download,
    file_name="meine_favoriten.csv",
    mime="text/csv"
)

# Kartenanzeige
st.markdown("---")
st.subheader("Favoriten als Karten")
cols = st.columns(3)
for idx, rezept in enumerate(favoriten):
    col = cols[idx % 3]
    with col:
        if rezept.get("strDrinkThumb"):
            st.image(rezept["strDrinkThumb"], width=120)
        st.markdown(f"**{rezept.get('strDrink', 'Unbekannter Drink')}**")
        if st.button("Rezept anzeigen", key=f"details_{idx}"):
            zutaten = []
            for i in range(1, 16):
                zutat = rezept.get(f"strIngredient{i}")
                menge = rezept.get(f"strMeasure{i}")
                if zutat and zutat.strip():
                    zutaten.append(f"- {menge or ''} {zutat}".strip())
            if zutaten:
                st.markdown("**Zutaten:**")
                for z in zutaten:
                    st.markdown(z)
            st.markdown("**Zubereitung:**")
            st.write(rezept.get("strInstructions", "Keine Anleitung vorhanden."))
