# Begrüßung des Benutzers
name = st.session_state.get('name', 'Gast')

# Begrüßung mit weißem Schatten um schwarzen Text
st.markdown(f"""
<div style='
    color: black;
    font-weight: bold;
    font-size: 1.8rem;
    text-shadow: 1px 1px 2px white, -1px -1px 2px white;
'>
✨ Hallo {name}! ✨
</div>
""", unsafe_allow_html=True)

# Einführungstext mit weißem Textschatten
st.markdown("""
<div style='
    color: black;
    font-size: 1.2rem;
    text-shadow: 1px 1px 2px white, -1px -1px 2px white;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
'>
Willkommen bei <b>Trink us</b>. Bei uns findest du zahlreiche Cocktails, die deinen Abend unvergesslich und geschmacksvoll machen.  
Für jeden Cocktail-Enthusiasten ist etwas dabei!!
</div>
""", unsafe_allow_html=True)

# Hinweis zum Alkoholkonsum (kann gestylt werden, aber st.info ist funktional gut)
st.info("""
##### **❗Hinweis zum Alkoholkonsum:❗**  
Diese Cocktailrezepte enthalten alkoholische Zutaten.  
Wenn du noch nicht volljährig bist, empfehlen wir dir, die Rezepte ohne Alkohol zuzubereiten als leckere Mocktail-Variante!  
Genieße verantwortungsvoll und altersgerecht. 🍸✨
""")

# Entwicklerhinweis mit weißem Schatten
st.markdown("""
<div style='
    color: black;
    font-size: 1rem;
    text-shadow: 1px 1px 2px white, -1px -1px 2px white;
    margin-top: 2rem;
'>
Diese App wurde von Carmen Hurschler, Mcqulat Miller und Joyce Baumann im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.
</div>
""", unsafe_allow_html=True)
