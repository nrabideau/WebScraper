# Syanpse Connect Program 

## Installation

### Prerequsite Downloads
* [google maps](https://pypi.org/project/googlemaps/)
* [PYYAML](https://pypi.org/project/PyYAML/)
* [pandas](https://pypi.org/project/pandas/)
* [Requests](https://pypi.org/project/requests/)
### API Keys Needed
* [Google Maps Places](https://developers.google.com/places/web-service/get-api-key)
* [YELP](https://www.yelp.com/developers)

## Running The Program
1. Place API keys in the [KEYS.YAML](keys.yaml)
*Should look like googlemaps: EXAMPLE_KEY With a space after :
2. Open the project, and select the import file (Should be Cunchbaseview.CSV)
3. Click begin to start scraping the data!

## Output
* Output will be in the Crunchbaseview.CSV file, all extra information will be shown here
* Extra Fields: Address, Lat/LONG, Phone, Website, Verified
* Verified shows if Google maps Matches YELP data, if yelp data does not match/exist value will be false
