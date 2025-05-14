import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Funktion zum Laden der Drinks aus JSON-Dateien
def load_drinks(file_paths):
    drinks = {}
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            drinks[data['name']] = 0  # Initialisiere Klicks mit 0
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
    # Pfade zu den JSON-Dateien der Cocktails und Mocktails
    cocktail_file = r'c:\Users\mcqul\OneDrive - ZHAW\Desktop\BMLD\2. Semester\Informatik 2\Übungen\Trinkuuus\Trink_us\Trink_us\drinks\Amaretto_Sour\rezept.json'
    mocktail_file = r'c:\Users\mcqul\OneDrive - ZHAW\Desktop\BMLD\2. Semester\Informatik 2\Übungen\Trinkuuus\Trink_us\Trink_us\drinks\Mocktail\rezept.json'

    # Drinks laden
    drink_clicks = load_drinks([cocktail_file, mocktail_file])

    # Simuliere Klicks
    click_drink("Amaretto Sour", drink_clicks)
    click_drink("Amaretto Sour", drink_clicks)
    click_drink("Mocktail", drink_clicks)

    # Statistik anzeigen
    plot_statistics(drink_clicks)