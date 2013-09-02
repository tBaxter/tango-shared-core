import urllib
import xmltramp

from django.conf import settings


def get_geocode(city, state, street_address="", zipcode=""):
    """
    For given location or object, takes address data and returns
    latitude and longitude coordinates from Google geocoding service

    get_geocode(self, street_address="1709 Grand Ave.", state="MO", zip="64112")

    Returns a tuple of (lat, long)
    Most times you'll want to join the return.

    """
    try:
        key = settings.GMAP_KEY
    except AttributeError:
        return "You need to put GMAP_KEY in settings"

    # build valid location string
    location = ""
    if street_address:
        location += '{}+'.format(street_address.replace(" ", "+"))
    location += '{}+{}'.format(city.replace(" ", "+"), state)
    if zipcode:
        location += "+{}".format(zipcode)

    url = "http://maps.google.com/maps/geo?q={}&output=xml&key={}".format(location, key)
    file = urllib.urlopen(url).read()
    try:
        xml = xmltramp.parse(file)
    except Exception as error:
        print("Failed to parse xml file {}: {}".format(file, error))
        return None

    status = str(xml.Response.Status.code)
    if status == "200":
        geocode = str(xml.Response.Placemark.Point.coordinates).split(',')
         # Flip geocode because geocoder returns long/lat while Maps wants lat/long.
         # Yes, it's dumb.
        return (geocode[1], geocode[0])
    else:
        print status
        return None
