import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

CLICK_FILE = "user_clicks.csv"

st.title("📊 Deine persönliche Drink-Statistik")

if "user" not in st.session_state:
    st.warning("Bitte zuerst einloggen.")
    st.stop()

user = st.session_state["user"]

# Klickdaten laden
if not os.path.exists(CLICK_FILE):
    st.info("Noch keine Klickdaten vorhanden.")
    st.stop()

df = pd.read_csv(CLICK_FILE, parse_dates=["timestamp"])
user_df = df[df["user"] == user]

if user_df.empty:
    st.info("Du hast noch keine Drinks geklickt.")
    st.stop()

# Gruppiere nach Drink und zähle Klicks
drink_stats = user_df.groupby("drink").size().sort_values(ascending=False)

# Diagramm anzeigen
fig, ax = plt.subplots(figsize=(10, 6))
drink_stats.plot(kind="bar", color="skyblue", ax=ax)
ax.set_title("Deine beliebtesten Drinks")
ax.set_xlabel("Drink")
ax.set_ylabel("Klicks")
plt.xticks(rotation=45)
st.pyplot(fig)
