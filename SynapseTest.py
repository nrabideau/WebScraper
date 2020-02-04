import csv
import os.path
import BusinessMapInfo
import pandas as pd
from os import path


def main():
    filename = 'crunch_bases_view.csv'
    deletetempFiles()
    initMapListCSV()
    initMissingEntriesCSV()
    importCSV(filename)

def getKey(keyName):
    with open (keys.yaml) as keyfile:
        data = yaml.safe_load(keyfile)
        print(data)

	

def importCSV(filename):
    names = []
    missingTemp = []
    mapsTemp = []

    print("WORKING....")
    with open(filename) as csv_file:
        line_count = 0
        NULL_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)

        names = csv_reader.__next__()  # grabs all of the values from the first row

        for row in csv_reader:
            line_count += 1
            missingTemp.clear()
            createmaplistCSV(row[7], row[11], mapsTemp)

            if "NULL" in row:
                # Put into seperate function task.
                # Location of row where business name is, we can change later to make this dynamic
                businessName = row[7]
                location = row[11]  # Where the business is located.
                for i in range(13, 25):
                    if row[i] == "NULL":
                        NULL_count += 1
                        missingTemp.append(names[i])
                        if i == 24:
                            createmissingCSV(
                                businessName, location, missingTemp)

        print("There are %d lines in the file" % (line_count))
        print("There are %d Nulls in the file" % (NULL_count))
        print("File Created")


def getaddressField(companyName, location):
    # This function will allow us to populate address, and lat/long
    # First param will be company name followed by location
    return(BusinessMapInfo.getAddress(companyName, location))


def getadditionalInfo(ID):
    # Function returns more data based on ID
    return (BusinessMapInfo.getadditionalInfo(ID))


def deletetempFiles():
    # Delete the old text file, so we can create a new one
    if (path.exists("missingentries.csv")):
        os.remove("missingentries.csv")
    if (path.exists("mapdata.csv")):
        os.remove("mapdata.csv")


def initMissingEntriesCSV():
    missingentries = open("missingentries.csv", "a+")
    missingentries.write(' Name, Location, Missing \n')


def createmissingCSV(businessName, location, missingTemp):
    missingentries = open("missingentries.csv", "a+")
    missingentries.write('"' + businessName + '",' + '"' +
                         location + '",')  # format proper
    for i in range(0, len(missingTemp)):
        missingentries.write('"')
        missingentries.write(missingTemp[i])
        missingentries.write('",')

    missingentries.write('\n')


# Output will be the company and map information.

def initMapListCSV():
    mapdata = open("mapdata.csv", "a+")
    mapdata.write('Name, Headquarters, Address, Phone, Website\n')


def createmaplistCSV(businessName, location, mapsTemp):
    mapsTemp.clear()
    locationData = getaddressField(businessName, location)
    mapdata = open("mapdata.csv", "a+")
    if (locationData['status'] == 'OK'):
        placeid = str(locationData['candidates'][0]['place_id'])
        # openingHours = str(locationData['candidates'][0]['opening_hours'])
        address = str(locationData['candidates'][0]['formatted_address'])
        # Gets more info like phone number and website
        additionalInfo = getadditionalInfo(placeid)

        phoneNumber = getPhoneNumber(additionalInfo)
        website = getWebsite(additionalInfo)

        mapsTemp.append(businessName)
        mapsTemp.append(location)
        mapsTemp.append(address)
        mapsTemp.append(phoneNumber)
        mapsTemp.append(website)

        print("found:" + businessName)
       
        for i in range(len(mapsTemp)):
            mapdata.write('"')
            mapdata.write(mapsTemp[i])
            mapdata.write('",')
        
        mapdata.write('\n')
    else:
        mapdata.write('"' + businessName + '",' + '"' + location +
                      '",'  + ' NULL , NULL , NULL \n')  # format proper

def getPhoneNumber(additionalInfo):
    try:
        return(additionalInfo['result']['formatted_phone_number'])

    except KeyError:
        return("NULL")


def getWebsite(additionalInfo):
    try:
        return(additionalInfo['result']['website'])

    except KeyError:
        return("NULL")


if __name__ == "__main__":
    main()
