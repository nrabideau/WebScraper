import csv
import os.path
import BusinessMapInfo
import pandas as pd
from os import path


def main():
    filename = 'crunch_bases_view.csv'
    deletetempFiles()
    importCSV(filename)


def importCSV(filename):
    names = ['id', 'created_at', 'updated_at', 'business_profile_id', 'business_profile_created', 'business_profile_updated', 'logo_import_status', 'name', 'url', 'categories', 'description',
             'headquarters_location', 'cb_rank', 'investor_type', 'investment_stage', 'number_of_employees', 'number_of_funding_rounds', 'funding_status', 'last_funding_date', 'last_funding_amount',
             'last_funding_type', 'total_funding_amount', 'number_of_lead_investors', 'number_of_investors', 'acquisition_status', 'operating_status']
    missingTemp = []
    print("WORKING....")
    with open(filename) as csv_file:
        line_count = 0
        NULL_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
        # col_Count = 26

        for row in csv_reader:
            line_count += 1
            missingTemp.clear()
            createmaplistCSV(row[7], row[11])
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


def deletetempFiles():
    # Delete the old text file, so we can create a new one
    if (path.exists("missingentries.csv")):
        os.remove("missingentries.csv")
    if (path.exists("mapdata.csv")):
        os.remove("mapdata.csv")


def createmissingCSV(businessName, location, missingTemp):
    missingentries = open("missingentries.csv", "a+")
    missingentries.write('"' + businessName + '",' + '"' + location +
                         '",')  # format proper
    for i in range(0, len(missingTemp)):
        missingentries.write('"')
        missingentries.write(missingTemp[i])
        missingentries.write('",')

    missingentries.write('\n')


# Output will be the company and map information.


def createmaplistCSV(businessName, location):
    locationData = getaddressField(businessName, location)
    mapdata = open("mapdata.csv", "a+")
    if (locationData['status'] == 'OK'):
        print("found:" + businessName)
        mapdata.write('"' + businessName + '",' + '"' + location +
                      '",' + '"' + str(locationData['candidates'][0]['formatted_address']) + '"\n')  # format proper
    else:
        mapdata.write('"' + businessName + '",' + '"' + location +
                      '",' + '"' + "NONE" + '"\n')  # format proper


if __name__ == "__main__":
    main()
