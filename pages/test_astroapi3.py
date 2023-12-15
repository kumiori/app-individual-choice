import datetime
from datetime import date
from typing import Union
import streamlit as st
import pytz
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
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

coordinates = (40.7127281, -74.0060152)
city_name = 'New York'
if coordinates:
    st.write(f"Coordinates for {city_name}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")

    timezone_finder = TimezoneFinder()
    timezone_str = timezone_finder.timezone_at(lat=coordinates[0], lng=coordinates[1])
    
    st.write(f"Time Zone: {timezone_str}")

    if timezone_str:
        tz = pytz.timezone(timezone_str)
        utc_offset = tz.utcoffset(datetime.now())
        st.write(f"UTC Offset: {utc_offset}")
else:
    st.warning("Coordinates not available.")
    
if timezone_str:
    tz = pytz.timezone(timezone_str)
    utc_offset = tz.utcoffset(datetime.now())
    offset_hours = utc_offset.seconds // 3600
    offset_minutes = (utc_offset.seconds % 3600) // 60
    current_time = datetime.now(tz)
    st.write(f"Current Time in {city_name}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    utc_offset = tz.utcoffset(current_time)
    st.write(f"UTC Offset: {utc_offset}")
    # Manually format the timezone offset
    offset_sign = '+' if offset_hours >= 0 else '-'
    offset_str = f'{offset_sign}{abs(offset_hours):02d}:{abs(offset_minutes):02d}'

    # Format the datetime object
    formatted_datetime = combined_datetime_utc.strftime(f'%Y-%m-%dT%H:%M:%S{offset_str}')

    st.write(f"Timezone Offset: {offset_str}")
    st.write("Formatted Datetime:", formatted_datetime)