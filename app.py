"""modules"""

import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API = os.getenv("WEATHER_API_KEY")

BASE_URL = "http://api.weatherapi.com/v1/current.json?key=" + API


@st.cache_data
def load_city_list():
    """
    Load a list of unique city names from a CSV file.

    Returns:
    list: A list of unique city names.
    """
    df = pd.read_csv(os.path.join(os.getcwd(), r"src\data\worldcities.csv"))
    return df["city"].dropna().unique().tolist()


def get_data(city: str):
    """
    Make a GET request to the base_url and return the JSON response object.
    If the response status code is not 200, raise an Exception with the detail
    from the JSON response object.
    """
    response = requests.get(BASE_URL, params={"q": city}, timeout=10)
    data = response.json()
    if response.status_code != 200:
        raise ValueError("sorry something went wrong")
    return data


def display_weather(data):
    """Display the current weather for a city."""
    col1, col2 = st.columns(2)
    col1.write(f"localtime: {data['location']['localtime']}")
    col1.write(f"City: {data['location']['name']}")
    col1.write(f"Temperature: {data['current']['temp_c']}°C")
    col2.write(f"Condition: {data['current']['condition']['text']}")
    col2.write(f"Wind Speed: {data['current']['wind_kph']} km/h")
    col2.write(f"Humidity: {data['current']['humidity']}%")


def home_page():
    """This function is the entry point for the Streamlit app.

    It displays a text input box for the user to enter a city name and
    then displays the current weather for that city.

    The function is decorated with @st.cache to store the results of the
    API call in memory so that subsequent calls with the same city name
    will not result in a new API call.

    :param city: The name of the city to get the weather for.
    :type city: str
    """
    cities = load_city_list()
    st.title("Weather App")
    city = st.selectbox("Enter a city:", cities)
    if st.button("Get Weather"):
        if city:
            try:
                data = get_data(city)
            except ImportError as e:
                st.error(e)
            else:
                display_weather(data)
        else:
            st.warning("Please enter a city name.")


if __name__ == "__main__":
    home_page()
