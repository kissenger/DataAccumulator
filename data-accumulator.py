
# Retrieves historical data from api, and adds new data to stored data so over time we can accumulate a longer time history
import requests
import json
from datetime import datetime
import sys, getopt

# symbol = "ADAUSD"
apiKey = "d50643f7000bdd881ebd539d4690b957"

# look for input arguments
# options for interval are: "1min", "5min", "15min", "30min", "1hour", "4hour"
try:
  opts, args = getopt.getopt(sys.argv[1:],"s:i:",["symbol=","interval="])
except getopt.GetoptError:
  print('data-accumulator.py -s <symbol> -i <interval>')
  sys.exit(2)
for opt, arg in opts:
  if opt in ("-s", "--symbol"):
    symbol = arg
  if opt in ("-i", "--interval"):
    interval = arg		

print('+++++++++++++++++++++++++++++++++++++++++')
print('Script run at: ' + str(datetime.now()) + ' for symbol: ' + symbol)

# Get New Data from API - https://financialmodelingprep.com/developer/docs/#Historical-Cryptocurrencies-Price
newData = requests.get("https://financialmodelingprep.com/api/v3/historical-chart/" + interval + "/" + symbol + "?apikey=" + apiKey).json()
fname=symbol+interval+".json"

# Read Saved Data Set - create a new saved file if it doesnt exist
try:
  with open(fname, "r") as infile:
    oldData = json.load(infile)
  print('Existing data file found, will add to that')
except IOError:
  with open(fname, "w") as outfile:
    json.dump(newData, outfile, indent=2)
  print('Data file not found, creating one')
  sys.exit()
except:
  print('unknown error reading data set')
  sys.exit()

# Find the last data point in the saved data set
latestSavedDate = oldData[0]['date']
print('Most recent time in existing data set is: ' + latestSavedDate)

# Find data newer than this in the new data set
i=0
while i < len(newData):
  if newData[i]['date']==latestSavedDate:
    uniqueData = newData[0:i]
    break
  i+=1

if i == len(newData):
  print('Most recent date not found, copying all data')
  uniqueData = newData
  
if i == 0:
  print('No new data found')
else:
  outfile = open(fname, "w")
  json.dump(uniqueData + oldData, outfile, indent=2)
  outfile.close()
  print('Added ' + str(len(uniqueData)) + ' new data points spanning ' + uniqueData[-1]['date'] + ' to ' + uniqueData[0]['date'])
