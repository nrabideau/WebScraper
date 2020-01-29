import csv
import os.path
from os import path
import BusinessMapInfo

def main():
    filename = 'crunch_bases_view.csv'
    deleteoldtextFile()
    importCSV(filename)
    addaddressField(filename)
    
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
            for i in range(col_Count):    #Put into seperate function task.
                if row[i] == "NULL": 
                    businessName = row[7] #Location of row where business name is, we can change later to make this dynamic
                    location = row[11]    #Where the business is located.
                    missingValue = names[i]
                    createtextFile(businessName, location, missingValue)
                    NULL_count +=1

        print("There are %d lines in the file" %(line_count))
        print("There are %d Nulls in the file" %(NULL_count))
        print("File Created" )

def addaddressField(filename):
#This function will allow us to populate address, and lat/long
     print(BusinessMapInfo.getAddress('Taco Bell','Largo'))#First param will be company name followed by location
         
          
def deleteoldtextFile():
#Delete the old text file, so we can create a new one
 if (path.exists("missingentries.txt")):
        os.remove("missingentries.txt")

def createtextFile(businessName, location, missingValue):
   
    missingentries = open("missingentries.txt","a+")
    missingentries.write(businessName + " " + location + " Missing :" + missingValue +"\n" )#format proper



if __name__== "__main__":
  main()
