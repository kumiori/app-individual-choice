import streamlit as st
import ipinfo

# Function to get location information based on IP address
def get_location_info():
    access_token = st.secrets["ipinfo"]["ACCESS_TOKEN"]  # Replace with your ipinfo.io access token
    handler = ipinfo.getHandler(access_token)

    # Get the information based on the user's IP address
    info = handler.getDetails()
    return info

def main():
    st.title("Streamlit App with Location")

    # Retrieve location information
    location_info = get_location_info()

    # Display the location information
    st.write(f"IP Address: {location_info.ip}")
    st.write(f"Location: {location_info.city}, {location_info.region}, {location_info.country}")
    st.write(f"Latitude: {location_info.latitude}, Longitude: {location_info.longitude}")
    st.write(f"Timezone {location_info.timezone}")
if __name__ == "__main__":
    main()
