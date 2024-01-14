from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import streamlit as st

coordinates = (40.7127281, -74.0060152)
city_name = 'New York'

if coordinates:
    st.write(f"Coordinates for {city_name}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")

    timezone_finder = TimezoneFinder()
    timezone_str = timezone_finder.timezone_at(lat=coordinates[0], lng=coordinates[1])
    st.write(f"Time Zone: {timezone_str}")

    if timezone_str:
        tz = pytz.timezone(timezone_str)

        # Get the current time in the specified time zone
        current_time_tz = datetime.now(tz)

        st.write(f"Current Time in {city_name}: {current_time_tz.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        utc_offset = tz.utcoffset(current_time_tz.replace(tzinfo=None))
        st.write(f"UTC Offset: {utc_offset}")
        # current_time = datetime.now(tz)  # Make the datetime object timezone-aware
        # utc_offset = tz.utcoffset(current_time)

        # Format the UTC offset as a string
        utc_offset_str = str(utc_offset)

        st.write(f"UTC Offset: {utc_offset_str}")
        
            
        # Convert the UTC offset to minutes
        utc_offset_minutes = utc_offset.total_seconds() / 60

        # Format the UTC offset as a string
        utc_offset_str = f"{int(utc_offset_minutes // 60):+03d}:{int(utc_offset_minutes % 60):02d}"

        st.write(f"UTC Offset: {utc_offset_str}")