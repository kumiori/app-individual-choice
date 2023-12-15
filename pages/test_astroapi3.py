import datetime
from datetime import date
from typing import Union
import streamlit as st
import sys
sys.path.append('lib/')
if 'timezone_offset' not in st.session_state:
    st.session_state.timezone_offset = 0  # Set the initial value to 0, you can set it to the default timezone offset

class Profile:
    def __init__(self, birth_date: Union[str, datetime], birth_time: str, birth_place: str):
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.birth_place = birth_place
        self.birth_datetime = self._get_birth_datetime()

    def _get_birth_datetime(self):
        if isinstance(self.birth_date, str):
            self.birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d')
        birth_datetime_str = f"{self.birth_date.strftime('%Y-%m-%d')} {self.birth_time}"
        return datetime.strptime(birth_datetime_str, '%Y-%m-%d %H:%M')

class Location:
    def __init__(self, latitude: float, longitude: float, altitude: float = 0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    @classmethod
    def from_address(cls, address: str):
        # You may use a geocoding service to get the latitude and longitude from the address
        # For simplicity, I'll assume the format "City, Country" and provide fixed values.
        # Replace this logic with a proper geocoding implementation.
        latitude, longitude = 0.0, 0.0
        return cls(latitude, longitude)

# Example usage:
# profile = Profile('1990-01-01', '12:30', 'New York, USA')
# location = Location.from_address('New York, USA')

import streamlit as st
from datetime import datetime, timedelta

col1, spacer, col2 = st.columns([1, .1, 1])

with col1:
    pass

with col2:
    birth_date = st.date_input("Birth Date")
    d = st.date_input("When's your birthday", date(2021, 3, 2))
    birth_time = st.text_input("Birth Time (24-hour format, e.g., 18:30)", "13:13")

# Combine date and time
combined_datetime = datetime.combine(birth_date, datetime.strptime(birth_time, "%H:%M").time())

# Convert to UTC (optional, depending on your use case)
combined_datetime_utc = combined_datetime - timedelta(minutes=int(st.session_state.timezone_offset))

# Format the datetime object to 'YYYY-MM-DDTHH:MM:SSZ'
formatted_datetime = combined_datetime_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

# Display the formatted datetime
st.write("Formatted Datetime:", formatted_datetime)
