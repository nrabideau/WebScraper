import googlemaps
from datetime import datetime
import json
key='Secret'

def getAddress(company_name, location): #Location here will give us the general location of the business. 
    #Place your API key here
    gmaps = googlemaps.Client(key=key)

    #We make the location bias only FL since that is our scope here.
    result_list = gmaps.find_place(company_name+location,'textquery',fields = ['formatted_address','opening_hours'],location_bias = 'rectangle:31.16816,-88.79009|25.02837,-79.40776')
    
    #Now we can return the address.

    return(result_list)
#This will get extra information about the company 
def getadditionalInfo(ID):

    gmaps = googlemaps.Client(key=key)

    result_list = gmaps.place(ID,'textquery',fields = ['formatted_phone_number','website'])

    return(result_list)
