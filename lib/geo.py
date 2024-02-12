from opencage.geocoder import OpenCageGeocode

def get_coordinates(api_key, city):
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.geocode(city)

    if results and len(results):
        first_result = results[0]
        lat, lng = first_result['geometry']['lat'], first_result['geometry']['lng']
        return lat, lng
    else:
        return None


def reverse_lookup(api_key, location):
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.reverse_geocode(location[0], location[1])

    if results and len(results):
        first_result = results[0]
        return results,
    else:
        return None