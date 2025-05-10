import streamlit as st

st.set_page_config(page_title="Cocktail Creator", page_icon="🍹", layout="centered")
st.title("🍸 Dein eigener Cocktail-Mixer")

# Cocktailname
cocktail_name = st.text_input("Gib deinem Cocktail einen Namen:")

# Basis-Spirituose
base = st.selectbox("Wähle deine Basis-Spirituose:", [
    "Rum", "Wodka", "Gin", "Tequila", "Whiskey", "Likör", "Ohne Alkohol"
])

st.divider()

# Zutaten-Auswahl (Standard + Eigene)
st.subheader("Zutaten auswählen oder eigene hinzufügen")

default_ingredients = [
    "Limettensaft", "Zitronensaft", "Orangensaft", "Ananassaft",
    "Cola", "Tonic Water", "Soda", "Zuckersirup",
    "Grenadine", "Minze", "Eiswürfel", "Ingwer", "Basilikum"
]

# Session State für Zutatenliste
if "custom_ingredients" not in st.session_state:
    st.session_state.custom_ingredients = []

# Anzeige der Zutaten (Standard + eigene)
all_ingredients = default_ingredients + st.session_state.custom_ingredients
selected_ingredients = st.multiselect("Wähle deine Zutaten:", all_ingredients)

# Eigene Zutat hinzufügen
with st.form("Eigene Zutat hinzufügen"):
    custom_input = st.text_input("Eigene Zutat:", placeholder="z. B. Lavendel, Matcha...")
    submitted = st.form_submit_button("➕ Hinzufügen")
    if submitted:
        if custom_input and custom_input not in st.session_state.custom_ingredients:
            st.session_state.custom_ingredients.append(custom_input)
            st.success(f"'{custom_input}' wurde hinzugefügt!")
        elif custom_input in st.session_state.custom_ingredients:
            st.warning("Diese Zutat wurde bereits hinzugefügt.")
        else:
            st.warning("Bitte gib eine gültige Zutat ein.")

st.divider()

# Deko
decoration = st.selectbox("Wähle eine Dekoration:", [
    "Limettenscheibe", "Cocktailkirsche", "Minzzweig", "Zuckerrand", "Keine"
])

# Cocktail mixen
if st.button("🍹 Cocktail mixen!"):
    if not cocktail_name:
        st.warning("Bitte gib deinem Cocktail einen Namen.")
    else:
        st.success(f"**{cocktail_name}** ist fertig gemixt!")
        st.markdown(f"""
        **Rezept für _{cocktail_name}_:**

        - **Basis:** {base}
        - **Zutaten:** {', '.join(selected_ingredients) if selected_ingredients else 'Keine'}
        - **Deko:** {decoration}
        """)
