import streamlit as st

# Seite konfigurieren (muss die erste Streamlit-Funktion sein)
st.set_page_config(page_title="Cocktail Creator", page_icon="🍹", layout="centered")

# CSS für das Formularfeld
form_css = """
<style>
div[data-testid="stForm"] {
    background-color: #8fbf93; /* Grün */
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
"""

# CSS in Streamlit einfügen
st.markdown(form_css, unsafe_allow_html=True)

st.title("🍸 Dein eigener Cocktail-Mixer")

# Standardzutaten
default_ingredients = [
    "Limettensaft", "Zitronensaft", "Orangensaft", "Ananassaft",
    "Cola", "Tonic Water", "Soda", "Zuckersirup",
    "Grenadine", "Minze", "Eiswürfel", "Ingwer", "Basilikum"
]

# Session State für eigene Zutaten
if "custom_ingredients" not in st.session_state:
    st.session_state.custom_ingredients = []

# Formular für die Cocktail-Gestaltung
with st.form("cocktail_form"):
    st.subheader("Gestalte deinen Cocktail 🍹")

    # Cocktailname
    cocktail_name = st.text_input("Gib deinem Cocktail einen Namen:")

    # Basis-Spirituose
    base = st.selectbox("Wähle deine Basis-Spirituose:", [
        "Rum", "Wodka", "Gin", "Tequila", "Whiskey", "Likör", "Ohne Alkohol"
    ])

    # Zutaten-Auswahl
    st.markdown("##### Zutaten auswählen oder eigene hinzufügen")
    all_ingredients = default_ingredients + st.session_state.custom_ingredients
    selected_ingredients = st.multiselect("Wähle deine Zutaten:", all_ingredients)

    # Eigene Zutat hinzufügen
    custom_input = st.text_input("Eigene Zutat hinzufügen:", placeholder="z. B. Lavendel, Matcha...")
    if st.form_submit_button("➕ Eigene Zutat hinzufügen"):
        if custom_input and custom_input not in st.session_state.custom_ingredients:
            st.session_state.custom_ingredients.append(custom_input)
            st.success(f"'{custom_input}' wurde hinzugefügt!")
        elif custom_input in st.session_state.custom_ingredients:
            st.warning("Diese Zutat wurde bereits hinzugefügt.")
        else:
            st.warning("Bitte gib eine gültige Zutat ein.")

    # Dekoration
    st.markdown("##### Dekoration auswählen")
    decoration = st.selectbox("Wähle eine Dekoration:", [
        "Limettenscheibe", "Cocktailkirsche", "Minzzweig", "Zuckerrand", "Keine"
    ])

    # Cocktail mixen Button
    submitted = st.form_submit_button("🍹 Cocktail mixen!")

# Ergebnis anzeigen
if submitted:
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