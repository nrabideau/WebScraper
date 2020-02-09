import csv
import os
import os.path
import BusinessMapInfo
import datetime
import pandas as pd  # Used
from os import path


def main():
    createtempFile()
    # Name of origional CSV file that will be fed in.
    filename = 'crunch_bases_view.csv'
    # Initializaion Functions
    deletetempFiles()
    initMapListCSV()
    initMissingEntriesCSV()
    # Main working function
    importCSV(filename)

# Function that creates our temp file Directory, that will be used to merge with main CSV file.


def createtempFile():
    path = os.getcwd()
    print(path)
    try:
        os.mkdir(path + "/tempoutputCSV")
    except OSError:
        print("Creation of the directory %s exists" % path)
    else:
        print("Successfully created the directory %s " % path)

# Call this function to get the path of the temp folder.


def getCSVfolderPath():
    return (os.getcwd() + "/tempoutputCSV/")


def importCSV(filename):
    # Arrays to populate the temp files
    names = []
    missingTemp = []
    mapsTemp = []

    print("WORKING....")
    with open(filename) as csv_file:
        line_count = 0
        NULL_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)

        # Get titles of the rows.
        names = csv_reader.__next__()

        # pandas data of the read csv file
        df = pd.read_csv(filename)
        for row in csv_reader:
            line_count += 1
            missingTemp.clear()
            # We need row[7] AKA company name and row[11] AKA location
            # Reccomend chaning this incase crunchabase pull changes row locations / rows added.

            # current date in YYYY-MM-DD format
            scanTime = datetime.date.today()

            # if 'updated_at' is not blank
            if row[2] != "":
                # last time this company was scanned
                oldTime = datetime.datetime.strptime(row[2], '%Y-%m-%d').date()
                # todays date - last scan date
                lastUpdate = scanTime-oldTime

            # if 'updated_at' is blank or is over 30 days old
            if(row[2] == "" or (lastUpdate > datetime.timedelta(days=30))):
                createmaplistCSV(row[7], row[11], mapsTemp)

                df.loc[df['id'] == line_count, ['updated_at']] = scanTime
                df.to_csv(filename, index=False)

                if "" in row:
                    # Put into seperate function task.
                    # Location of row where business name is, we can change later to make this dynamic
                    businessName = row[7]
                    location = row[11]  # Where the business is located.
                    # This loop creates a log of all the missing values we can find later
                    for i in range(13, 25):
                        if row[i] == "":
                            NULL_count += 1
                            missingTemp.append(names[i])
                            if i == 24:
                                createmissingCSV(
                                    businessName, location, missingTemp)

            # if 'updated_at' is not blank and is not 30 days old
            elif(row[2] != "" and (lastUpdate < datetime.timedelta(days=30))):
                print("Skipping " + row[7] + ", last updated on " + row[2])

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
    if (path.exists(getCSVfolderPath() + "missingentries.csv")):
        os.remove(getCSVfolderPath() + "missingentries.csv")
    if (path.exists(getCSVfolderPath() + "mapdata.csv")):
        os.remove(getCSVfolderPath() + "mapdata.csv")
    # if (path.exists(getCSVfolderPath() + "updateLog.csv")):
    #   os.remove(getCSVfolderPath() + "updateLog.csv")

# Future use CSV for finding missing values using a web scraper.


def initMissingEntriesCSV():
    missingentries = open(getCSVfolderPath() + "missingentries.csv", "a+")
    missingentries.write(' Name, Location, Missing \n')

# write the missing entries to the file we just created in initMissingEntriesCSV


def createmissingCSV(businessName, location, missingTemp):
    missingentries = open(getCSVfolderPath() + "missingentries.csv", "a+")
    missingentries.write('"' + businessName + '",' + '"' +
                         location + '",')  # format proper
    for i in range(0, len(missingTemp)):
        missingentries.write('"')
        missingentries.write(missingTemp[i])
        missingentries.write('"')

        if i < len(missingTemp) - 1:
            missingentries.write(',')

    missingentries.write('\n')


# Output will be the company and map information. including phone number, website, address.
# This function creates row 1 header.
def initMapListCSV():
    mapdata = open(getCSVfolderPath() + "mapdata.csv", "a+")
    mapdata.write(
        'Name, Headquarters, Address, LAT/LONG,Phone, Website\n')

# Populate the rest of the feilds with location informaion.


def createmaplistCSV(businessName, location, mapsTemp):
    mapsTemp.clear()
    mapdata = open(getCSVfolderPath() + "mapdata.csv", "a+")
    locationData = getaddressField(businessName, location)
    # API call to google maps, if this check passes means that the company matches.
    if (locationData['status'] == 'OK'):
        # Grab the first canidate, since it will be the closest match.
        placeid = str(locationData['candidates'][0]['place_id'])
        address = str(locationData['candidates'][0]['formatted_address'])
        geometry = str(locationData['candidates'][0]['geometry'])
        # closed = str(locationData['candidates'][0]['permanently_closed'])

        # Make another API call to get additional info about the company.
        additionalInfo = getadditionalInfo(placeid)
        phoneNumber = getPhoneNumber(additionalInfo)
        website = getWebsite(additionalInfo)
        # Add all this new info to our array, which we use to populate map info.
        # Any additional info from a maps API call should go here.
        mapsTemp.append(businessName)
        mapsTemp.append(location)
        mapsTemp.append(address)
        mapsTemp.append(geometry)
        mapsTemp.append(phoneNumber)
        mapsTemp.append(website)

        print("found:" + businessName)
        # Properly format the Array into a CSV type.
        for i in range(len(mapsTemp)):
            mapdata.write('"')
            mapdata.write(mapsTemp[i])
            mapdata.write('"')
            if i < len(mapsTemp) - 1:
                mapdata.write(',')

        mapdata.write('\n')

    # This means the company was not found
    elif (locationData['status'] == 'ZERO_RESULTS'):
        mapdata.write('"' + businessName + '",' + '"' + location +
                      '",' + '  \n')  # format proper

    else:  # Some kind of other error occured.
        print("GMAP ERROR RETRY...")


def getPhoneNumber(additionalInfo):
    try:
        return(additionalInfo['result']['formatted_phone_number'])

    except KeyError:
        return("")


def getWebsite(additionalInfo):
    try:
        return(additionalInfo['result']['website'])

    except KeyError:
        return("")


if __name__ == "__main__":
    main()
