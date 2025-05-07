import streamlit as st

# Titel der Seite
st.title("Favoriten")

# Beschreibung
st.write("Hier können Sie Ihre Lieblingsrezepte speichern und verwalten.")

# Favoriten-Liste initialisieren
if "favoriten" not in st.session_state:
    st.session_state["favoriten"] = []

# Eingabefelder für neues Rezept
rezept_titel = st.text_input("Titel des Rezepts:")
rezept_beschreibung = st.text_area("Beschreibung des Rezepts:")

# Button zum Hinzufügen eines Rezepts
if st.button("Rezept hinzufügen"):
    if rezept_titel and rezept_beschreibung:
        neues_rezept = {"titel": rezept_titel, "beschreibung": rezept_beschreibung}
        st.session_state["favoriten"].append(neues_rezept)
        st.success(f"Rezept '{rezept_titel}' wurde hinzugefügt!")
    else:
        st.error("Bitte geben Sie sowohl einen Titel als auch eine Beschreibung ein.")

# Gespeicherte Rezepte anzeigen
st.write("### Ihre gespeicherten Rezepte:")
if st.session_state["favoriten"]:
    for rezept in st.session_state["favoriten"]:
        st.write(f"**{rezept['titel']}**")
        st.write(rezept["beschreibung"])
        st.write("---")
else:
    st.write("Noch keine Favoriten gespeichert.")