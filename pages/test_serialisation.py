# import streamlit 
import json
from datetime import datetime

response_data = {
  "signature": {
    "label": "Signature",
    "value": "e8960f96b2f44539b070a87a32c644357c39374d3605b61f25e8c73c24cdbd65"
  },
  "name": {
    "label": "Name",
    "value": "ALB"
  },
  "email": {
    "label": "Email",
    "value": "leon.baldelli@cnrs.fr"
  },
  "phone": {
    "label": "Phone Number (starting with +)",
    "value": ""
  },
  "athena-range-dates": {
    "label": "",
    "value": [
      "datetime.date(2024, 9, 24)",
      "datetime.date(2024, 9, 29)"
    ]
  },
  "extra": {
    "label": "Any additional comments or preferences?",
    "value": ""
  }
}

print(json.dumps(response_data, indent=2))


# # Deserialize the date strings in the response_data
# for key, value in response_data.items():
#     if isinstance(value.get("value"), list):
#         # Deserialize each date string in the list
#         deserialized_dates = [eval(date_str) if date_str.startswith("datetime.date") else date_str for date_str in value["value"]]
#         response_data[key]["value"] = deserialized_dates

# # Print the updated response_data
# print(json.dumps(response_data, indent=2))
