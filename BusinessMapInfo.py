import googlemaps
from datetime import datetime
import json
import keyfile
# Key to get goolemaps data. To change API key modify keys.yaml file
key = (keyfile.getKey('googlemaps'))


# Location here will give us the general location of the business.
def getAddress(company_name, location):
    gmaps = googlemaps.Client(key=key)

    # We make the location bias only FL since that is our scope here.
    result_list = gmaps.find_place(company_name+location, 'textquery', fields=[
                                   'formatted_address', 'place_id', 'geometry/location'], location_bias='rectangle:31.16816,-88.79009|25.02837,-79.40776')

    # Now we can return the address , place id (Used to do another API call for more information),Geometry is LAT/LONG

    return(result_list)


# This funtion will get extra information about the company
def getadditionalInfo(ID):

    gmaps = googlemaps.Client(key=key)

    result_list = gmaps.place(ID, 'textquery', fields=[
                              'formatted_phone_number', 'website', 'opening_hours'])

    return(result_list)
