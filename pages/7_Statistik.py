import matplotlib.pyplot as plt
from collections import defaultdict
from Cocktail_library import get_cocktails  # Importiere die Cocktails aus der Cocktail-Bibliothek
from Mocktail_library import get_mocktails  # Importiere die Mocktails aus der Mocktail-Bibliothek

# Funktion zum Laden der Drinks aus den Bibliotheken
def load_drinks():
    drinks = {}
    # Cocktails laden
    cocktails = get_cocktails()
    for cocktail in cocktails:
        drinks[cocktail['name']] = 0  # Initialisiere Klicks mit 0

    # Mocktails laden
    mocktails = get_mocktails()
    for mocktail in mocktails:
        drinks[mocktail['name']] = 0  # Initialisiere Klicks mit 0

    return drinks

# Funktion zum Simulieren eines Klicks auf einen Drink
def click_drink(drink_name, drink_clicks):
    if drink_name in drink_clicks:
        drink_clicks[drink_name] += 1

# Funktion zum Erstellen eines Säulendiagramms
def plot_statistics(drink_clicks):
    drinks = list(drink_clicks.keys())
    clicks = list(drink_clicks.values())

    plt.figure(figsize=(10, 6))
    plt.bar(drinks, clicks, color='skyblue')
    plt.xlabel('Drinks', fontsize=12)
    plt.ylabel('Häufigkeit (Klicks)', fontsize=12)
    plt.title('Häufigkeit der Drinks', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Hauptprogramm
if __name__ == "__main__":
    # Drinks laden
    drink_clicks = load_drinks()

    # Simuliere Klicks
    click_drink("Amaretto Sour", drink_clicks)
    click_drink("Amaretto Sour", drink_clicks)
    click_drink("Mocktail", drink_clicks)

    # Statistik anzeigen
    plot_statistics(drink_clicks)