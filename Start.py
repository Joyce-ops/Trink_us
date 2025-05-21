# Begrüßung des Benutzers
name = st.session_state.get('name', 'Gast')

# Begrüßung – fett & größer
st.markdown(f"""
<div style='
    color: black;
    font-weight: 900;
    font-size: 2rem;
'>
✨ Hallo {name}! ✨
</div>
""", unsafe_allow_html=True)

# Einführungstext – fett & gut lesbar
st.markdown("""
<div style='
    color: black;
    font-weight: 600;
    font-size: 1.3rem;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
'>
Willkommen bei <b>Trink us</b>. Bei uns findest du zahlreiche Cocktails, die deinen Abend unvergesslich und geschmacksvoll machen.  
Für jeden Cocktail-Enthusiasten ist etwas dabei!!
</div>
""", unsafe_allow_html=True)

# Hinweis zum Alkoholkonsum (funktional mit st.info belassen)
st.info("""
##### **❗Hinweis zum Alkoholkonsum:❗**  
Diese Cocktailrezepte enthalten alkoholische Zutaten.  
Wenn du noch nicht volljährig bist, empfehlen wir dir, die Rezepte ohne Alkohol zuzubereiten als leckere Mocktail-Variante!  
Genieße verantwortungsvoll und altersgerecht. 🍸✨
""")

# Entwicklerhinweis – auch etwas fetter
st.markdown("""
<div style='
    color: black;
    font-weight: 600;
    font-size: 1rem;
    margin-top: 2rem;
'>
Diese App wurde von Carmen Hurschler, Mcqulat Miller und Joyce Baumann im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.
</div>
""", unsafe_allow_html=True)
