import pytz
from datetime import datetime

def get_utc_offset(timezone_str):
    # Create a datetime object for the current time
    now = datetime.now()

    # Get the timezone object for the specified timezone string
    tz = pytz.timezone(timezone_str)

    # Get the UTC offset for the current time
    utc_offset_timedelta = tz.utcoffset(now)

    # Convert the timedelta to hours and minutes
    total_minutes = utc_offset_timedelta.total_seconds() / 60
    hours, minutes = divmod(total_minutes, 60)

    # Format the UTC offset string
    utc_offset_str = "{:02d}:{:02d}".format(int(hours), int(minutes))

    return utc_offset_str

# Example usage
timezone_str = "America/New_York"
utc_offset = get_utc_offset(timezone_str)
print(f"UTC offset for {timezone_str}: {utc_offset}")


