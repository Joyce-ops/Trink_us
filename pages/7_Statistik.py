import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Pfad zur Datei mit den Klickdaten
CLICK_FILE = "user_clicks.csv"

# Titel
st.title("📊 Deine persönliche Drink-Statistik")

# Überprüfe, ob der Benutzer eingeloggt ist
if "user" not in st.session_state:
    st.warning("Bitte zuerst einloggen.")
    st.stop()

# Aktuellen Benutzer aus dem Session State holen
user = st.session_state["user"]

# Prüfe, ob die Klickdaten existieren
if not os.path.exists(CLICK_FILE):
    st.info("Noch keine Klickdaten vorhanden.")
    st.stop()

# Lade die CSV-Datei mit Klickdaten
df = pd.read_csv(CLICK_FILE, parse_dates=["timestamp"])

# Filtere die Daten für den eingeloggten Benutzer
user_df = df[df["user"] == user]

# Zeige Info, wenn der Benutzer keine Klicks hat
if user_df.empty:
    st.info("Du hast noch keine Drinks geklickt.")
    st.stop()

# Gruppiere nach Drink und zähle Klicks
drink_stats = user_df.groupby("drink").size().sort_values(ascending=False)

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 6))
drink_stats.plot(kind="bar", color="skyblue", ax=ax)

# Diagramm beschriften
ax.set_title("Deine beliebtesten Drinks")
ax.set_xlabel("Drink")
ax.set_ylabel("Klicks")
plt.xticks(rotation=45)

# Diagramm in Streamlit anzeigen
st.pyplot(fig)
