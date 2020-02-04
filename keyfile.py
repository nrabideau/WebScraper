import yaml #this is so every time we upload we dont have to copy paste the key
#This file is used to retreive different keys from files, simply pass the name of the key you want as a parameter. 
def getKey(keyName):
    
    with open ('keys.yaml','r') as keyfile:
        data = yaml.safe_load(keyfile) 
        return(data[keyName])

        