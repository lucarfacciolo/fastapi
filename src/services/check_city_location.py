# external
# from geopy.geocoders import Nominatim


def city_in_usa(city: str) -> bool:
    # (NOTE lfacciolo) could use geopy if USA not in name, this will make creation slower
    if "(USA)" in city:
        return True
    return False
