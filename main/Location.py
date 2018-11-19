import geocoder


def get_location():
    g = geocoder.ip('me')
    j = g.geojson

    return j.get('features')[0].get('properties').get('address')