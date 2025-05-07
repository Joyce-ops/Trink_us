import streamlit as st

# Titel der Seite
st.title("Favoriten")

# Beschreibung
st.write("Hier können Sie Ihre Lieblingsrezepte speichern und verwalten.")

# Favoriten-Liste initialisieren
if "favoriten" not in st.session_state:
    st.session_state["favoriten"] = []

# Eingabefeld für neues Rezept
rezept_titel = st.text_input("Titel des Rezepts:")

# Automatisches Hinzufügen des Rezepts, wenn ein Titel eingegeben wird
if rezept_titel:
    # Überprüfen, ob das Rezept bereits existiert
    if not any(rezept["titel"] == rezept_titel for rezept in st.session_state["favoriten"]):
        # Rezept automatisch erstellen
        neues_rezept = {
            "titel": rezept_titel,
            "beschreibung": f"Automatisch generiertes Rezept für {rezept_titel}."
        }
        st.session_state["favoriten"].append(neues_rezept)
        st.success(f"Rezept '{rezept_titel}' wurde hinzugefügt!")
    else:
        st.warning(f"Das Rezept '{rezept_titel}' ist bereits in den Favoriten gespeichert.")

# Gespeicherte Rezepte anzeigen
st.write("### Ihre gespeicherten Rezepte:")
if st.session_state["favoriten"]:
    for index, rezept in enumerate(st.session_state["favoriten"]):
        st.write(f"**{rezept['titel']}**")
        # Button für jedes Rezept
        if st.button(f"Details zu '{rezept['titel']}' anzeigen", key=f"details_{index}"):
            st.write(rezept["beschreibung"])
        st.write("---")
else:
    st.write("Noch keine Favoriten gespeichert.")