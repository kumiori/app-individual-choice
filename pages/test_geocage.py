from opencage.geocoder import OpenCageGeocode
import streamlit as st

def get_coordinates(api_key, city):
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.geocode(city)

    if results and len(results):
        first_result = results[0]
        lat, lng = first_result['geometry']['lat'], first_result['geometry']['lng']
        return lat, lng
    else:
        return None

# Replace 'your_api_key' with your actual OpenCage API key
city_name = 'New York'  # Replace with the desired city name

coordinates = get_coordinates(st.secrets("OPENCAGE_KEY"), city_name)
st.write(coordinates)

if coordinates:
    st.write(f"Coordinates for {city_name}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
else:
    st.write(f"Coordinates not found for {city_name}")