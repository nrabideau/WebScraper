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
    names = ['id','created_at','updated_at','business_profile_id','business_profile_created','business_profile_updated','logo_import_status','name','url' ,'categories','description',
               'headquarters_location','cb_rank','investor_type','investment_stage','number_of_employees','number_of_funding_rounds','funding_status','last_funding_date','last_funding_amount',
               'last_funding_type', 'total_funding_amount','number_of_lead_investors','number_of_investors' ,'acquisition_status','operating_status']
    print("WORKING....")
    with open(filename) as csv_file:
        line_count = 0
        NULL_count = 0
        csv_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
        col_Count = 26

        for row in csv_reader:
            line_count +=1

            createmaplistCSV(row[7],row[11])
            
            for i in range(col_Count):    #Put into seperate function task.
                if row[i] == "NULL": 
                    businessName = row[7] #Location of row where business name is, we can change later to make this dynamic
                    location = row[11]    #Where the business is located.
                    missingValue = names[i]
                    createmissingCSV(businessName, location, missingValue)
                    NULL_count +=1
       

        print("There are %d lines in the file" %(line_count))
        print("There are %d Nulls in the file" %(NULL_count))
        print("File Created" )

def getaddressField(companyName,location):
#This function will allow us to populate address, and lat/long
     return(BusinessMapInfo.getAddress(companyName,location))#First param will be company name followed by location
         
          
def deletetempFiles():
#Delete the old text file, so we can create a new one
 if (path.exists("missingentries.csv")):
        os.remove("missingentries.csv")
 if (path.exists("mapdata.csv")):
        os.remove("mapdata.csv")


def createmissingCSV(businessName, location, missingValue):
    missingentries = open("missingentries.csv","a+")
    missingentries.write('"' + businessName + '",' + '"' + location + '",' + '"' + missingValue + '"\n' )#format proper
#Output will be the company and map information.

def createmaplistCSV(businessName,location):
    locationData = getaddressField(businessName,location)
    mapdata = open("mapdata.csv","a+")
    if (locationData):
        print("found:" + businessName)
        mapdata.write('"' + businessName + '",' + '"' + location + '",' + '"' + str(locationData) + '"\n' )#format proper
    else:
        mapdata.write('"' + businessName + '",' + '"' + location + '",' + '"' + "NONE" + '"\n' )#format proper

  
    
if __name__== "__main__":
  main()
