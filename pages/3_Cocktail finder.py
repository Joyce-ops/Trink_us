import requests

import streamlit as st

import pandas as pd
 
API = "https://www.thecocktaildb.com/api"
 
def get_cocktails(cocktail_name=None):

    api_url = f"{API}/json/v1/1/search.php?s={cocktail_name}"

    response = requests.get(api_url)

    if response.status_code == 200:

        try:

            data = response.json()

            return data

        except requests.exceptions.JSONDecodeError:

            st.error("Invalid response from API. Could not decode JSON.")

            return None

    else:

        st.error(f"Error fetching data from API. Status code: {response.status_code}")

        return None
 
 
def main():

    st.title("Cocktail Rezept Finder")

    cocktail_name = st.text_input("Gib den Cocktail Namen ein:")

    if st.button("Rezept"):

        if cocktail_name:

            data = get_cocktails(cocktail_name)

            if data:

                drinks = [data['drinks'][i] for i in range(len(data['drinks']))]

                drinks_df = pd.DataFrame(drinks)

                drinks = [data['drinks'][i] for i in range(len(data['drinks']))]

                drinks_df = pd.DataFrame(drinks)

                # Display cocktail images

                st.subheader("Cocktail Recipes")

                columns = st.columns(4)

                for index, row in drinks_df.iterrows():

                    col = columns[index % 4]  # Cycle through the 4 columns

                    with col:

                        cocktail_name = row['strDrink']

                        cocktail_image = row['strDrinkThumb']

                        st.image(cocktail_image, caption=cocktail_name, use_container_width=True)
 
            else:

                st.error("No cocktail found with that name.")

        else:

            st.error("Please enter a cocktail name.")


if __name__ == "__main__":

    main()
 