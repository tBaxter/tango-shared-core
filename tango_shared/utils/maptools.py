from __future__ import print_function

import urllib

from django.conf import settings

import untangle


def get_geocode(city, state, street_address="", zipcode=""):
    """
    For given location or object, takes address data and returns
    latitude and longitude coordinates from Google geocoding service

    get_geocode(self, street_address="1709 Grand Ave.", state="MO", zip="64112")

    Returns a tuple of (lat, long)
    Most times you'll want to join the return.

    """
    keytype = None
    url = None
    # build valid location string
    location = ""
    if street_address:
        location += '{}+'.format(street_address.replace(" ", "+"))
    location += '{}+{}'.format(city.replace(" ", "+"), state)
    if zipcode:
        location += "+{}".format(zipcode)
    
    # Resolve which API to use
    if hasattr(settings, GMAP_KEY):
        key = settings.GMAP_KEY
        keytype = 'Google'
        url = 'https://maps.googleapis.com/maps/api/geocode/xml?address={}&key={}'.format(location, key)
        try:
            xml = untangle.parse(url)
        except Exception as error:
            print("Failed to parse Google xml file {}: {}".format(url, error))
            return None
        status = str(xml.Response.Status.code)
        if status == "200":
            geocode = str(xml.Response.Placemark.Point.coordinates).split(',')
            # Flip geocode because geocoder returns long/lat while Maps wants lat/long.
            # Yes, it's dumb.
            return (geocode[1], geocode[0])
        
    elif hasattr(settings, LOCATIONIQ_KEY):
        key = settings.LOCATIONIQ_KEY
        keytype = "LocationIQ"
        url = 'https://us1.locationiq.com/v1/search.php?key={}&q={}&format=xml'.format(key, location)
        try:
            xml = untangle.parse(url)
        except Exception as error:
            print("Failed to parse LocationIQ xml file {}: {}".format(url, error))
            return None
        if xml.searchresults.place:
            lat = xml.searchresults.place['lat']
            lon = xml.searchresults.place['lon']
            return (lat, lon)
    else:
        return "You need to put GMAP_KEY or LOCATIONIQ_KEY in settings."

