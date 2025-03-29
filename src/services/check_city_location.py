from geopy.geocoders import Nominatim


def city_in_usa(city: str) -> bool:
    if "(USA)" in city:
        return True
    return False
