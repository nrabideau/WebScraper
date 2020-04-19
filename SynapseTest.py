import csv
import os
import os.path
import BusinessMapInfo
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import pandas as pd  # Used for csv editing
from os import path
from difflib import SequenceMatcher  # to compare strings
from tkinter import messagebox

filename = ''


def main():
    createtempFile()
    # Name of origional CSV file that will be fed in.
    createGUI()
    # Initializaion Functions
    if (filename == ''):
        showError()
        return 0

    deletetempFiles()

    if (testAPI("largo", "Taco Bell", "9999999999")):  # Testing APIs, info can be whatever

        initMapListCSV()
        initMissingEntriesCSV()
    # Main working function
        importCSV(filename)
    # Place Functions for more scrape data below...
        cleanup()
    else:
        return 0
# Function that creates our temp file Directory, that will be used to merge with main CSV file.


def showError():
    root = Tk()
    root.withdraw()
    messagebox.showerror("Error", "Before staring parse, select input file...")


def createGUI():

    root = Tk()
    frame = tk.Frame(root)
    frame.pack()
    root.title("Synapse Data Scraper")
    button = tk.Button(frame,
                       text="QUIT PROGRAM",
                       fg="red",
                       command=quit)
    button.pack(side=tk.LEFT)

    filename = tk.Button(frame,
                         text="Select Input File",
                         command=getFilename
                         )
    filename.pack(side=tk.LEFT)

    start = tk.Button(frame,
                      text="Start parse",
                      command=root.destroy
                      )
    start.pack(side=tk.LEFT)

    root.mainloop()

    return filename


def getFilename():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(
    ), title="Select file", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))


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

        if(len(names) == 26):
            df["Address"] = ""
            df["Lat/Long"] = ""
            df["Phone"] = ""
            df["Website"] = ""
            df["Verified"] = ""
            df.to_csv(filename, index=False)

        for row in csv_reader:
            line_count += 1
            missingTemp.clear()
            # We need row[7] AKA company name and row[11] AKA location
            checkDate(names, mapsTemp, missingTemp, filename, row, df, line_count,
                      NULL_count)


def checkDate(names, mapsTemp, missingTemp, filename, row, df, line_count, NULL_count):

    # current date in MM-DD-YYYY format
    scanTime = datetime.date.today()

    # sets crated_at with current date if this is the first scan
    if row[1] == "":
        print("\nFirst time scanning %s, scan on %s: " %
              (str(row[7]), str(scanTime.strftime('%m/%d/%Y'))))

        df.loc[df['id'] == line_count, ['created_at']
               ] = scanTime.strftime('%m/%d/%Y')

    # if 'updated_at' is not blank
    if row[2] != "":
        # last time this company was scanned
        oldTime = datetime.datetime.strptime(row[2], '%m/%d/%Y').date()
        # todays date - last scan date
        lastUpdate = scanTime-oldTime

    # if 'updated_at' is blank or is over 30 days old
    if(row[2] == "" or (lastUpdate > datetime.timedelta(days=30))):
        createmaplistCSV(row[7], row[11], mapsTemp, df, line_count)

        df.loc[df['id'] == line_count, ['updated_at']
               ] = scanTime.strftime('%m/%d/%Y')

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
        'Name, Headquarters, Address, LAT/LONG, Phone, Website, Yelp Match\n')

# Populate the rest of the feilds with location informaion.


def testAPI(location, name, phone):
    try:
        print("Testing google MAPS API")
        getaddressField(name, location)
    except:
        print("GOOGLE MAPS API ERROR")
        return False

    try:
        print("Testing YELP API")
        BusinessMapInfo.getYelpInfo("9999999999")
    except:
        print("YELP API ERROR")
        return False

    print("BOTH APIs Valid...")
    return True


def createmaplistCSV(businessName, location, mapsTemp, df, line_count):
    mapsTemp.clear()
    mapdata = open(getCSVfolderPath() + "mapdata.csv", "a+")

    locationData = getaddressField(businessName, location)

    # API call to google maps, if this check passes means that the company matches.
    if (locationData['status'] == 'OK'):
        # Grab the first canidate, since it will be the closest match.
        placeid = str(locationData['candidates'][0]['place_id'])
        address = str(locationData['candidates'][0]['formatted_address'])
        geometry = str(locationData['candidates'][0]['geometry'])

        # Make another API call to get additional info about the company.
        additionalInfo = getadditionalInfo(placeid)
        phoneNumber = getPhoneNumber(additionalInfo)
        website = getWebsite(additionalInfo)
        # Add all this new info to our array, which we use to populate map info.
        # Any additional info from a maps API call should go here.

        print("Found on Google Maps")

        mapsTemp.append(businessName)
        mapsTemp.append(location)
        mapsTemp.append(address)
        mapsTemp.append(geometry)
        mapsTemp.append(phoneNumber)
        mapsTemp.append(website)

        df.loc[df['id'] == line_count, ['Address']
               ] = address

        df.loc[df['id'] == line_count, ['Lat/Long']
               ] = geometry

        df.loc[df['id'] == line_count, ['Phone']
               ] = phoneNumber

        df.loc[df['id'] == line_count, ['Website']
               ] = website

        if (phoneNumber != 'NULL' or phoneNumber != ""):

            yelpResponse = BusinessMapInfo.getYelpInfo(phoneNumber)

            # If no response with phone number, it will throw a keyerror
            try:
                total = yelpResponse["total"]
            except KeyError:
                total = 0

            if (total > 0):
                print("Comparing Yelp To GMAPS data")
                # Check to see if Yelp data matches google maps
                yelpReturn = comparison(
                    address, businessName, phoneNumber, yelpResponse)

                if (yelpReturn):
                    print("Yelp data matches Google maps\n")
                    mapsTemp.append("true")
                    df.loc[df['id'] == line_count, ['Verified']
                           ] = "True"

                else:
                    mapsTemp.append("false")
                    print("no match ON YELP")
                    df.loc[df['id'] == line_count, ['Verified']
                           ] = "False"
            else:
                mapsTemp.append("false")
                print("no match ON YELP")
                df.loc[df['id'] == line_count, ['Verified']
                       ] = "False"
        else:
            print("no match ON YELP")
            df.loc[df['id'] == line_count, ['Verified']
                   ] = "False"

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
        print("No results on google maps")
        mapdata.write('"' + businessName + '",' + '"' + location +
                      '",' + '  \n')  # format proper

    else:  # Some kind of other error occured.
        print("GMAP ERROR RETRY...")


def comparison(Gmaps, googlebusinessName, gmapPhone, yelp):

    gmapAddress = Gmaps  # str(Gmaps['candidates'][0]['formatted_address'])
    gmapCompanyName = str(googlebusinessName)

    print("Comparing against %s, %s, %s" %
          (gmapCompanyName, gmapAddress, gmapPhone))

    for i in range(0, len(yelp["businesses"])):
        yelpAddress = str(yelp["businesses"][i]["location"]["display_address"])
        yelpAddress += ", United States"
        yelpCompanyName = str(yelp["businesses"][i]["name"])
        yelpPhone = str(yelp["businesses"][i]["phone"])

        print("Comparing: %s, %s, %s" %
              (yelpCompanyName, yelpAddress, yelpPhone))
        # address is formateed differently, than Gmaps
        yelpAddresslength = len(yelpAddress)
        # next, we cut down the google map sting to correct length
        gmapAddress = gmapAddress[:yelpAddresslength]

        addressScore = SequenceMatcher(a=yelpAddress, b=gmapAddress).ratio()
        nameScore = SequenceMatcher(
            a=yelpCompanyName, b=gmapCompanyName).ratio()
        if(addressScore >= .75 and nameScore >= .60):
            yelpReturn = [yelpCompanyName, yelpAddress, yelpPhone]
            return yelpReturn

    return False


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


def cleanup():
    print("Search Complete, cleaning up...")
    # Add Cleanup logic deleting files, ETC...


if __name__ == "__main__":
    main()
