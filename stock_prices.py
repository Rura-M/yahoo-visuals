import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine

# Check to see if a connection is established
def fetchStockData(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"
    
    headers = {
    'x-rapidapi-key': "4b9c386372msh305d0f5e33cb633p1cee26jsn477776e57ef8",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    querystring = {"region": "US", "symbol": symbol, "interval": "1d", "range": "3mo"}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
      return response.json()
    else:
      return None
    
def parseTimestamp(inputdata):
      timestamplist = []
      timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
      timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
      calendertime = []
      for ts in timestamplist:
        dt = datetime.fromtimestamp(ts)
        calendertime.append(dt.strftime("%m/%d/%Y"))
      return calendertime
    
def parseValues(inputdata):
      valueList = []
      valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
      valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])
      return valueList 
    
def attachEvents(inputdata):
      eventlist = []
      for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("open")  
      for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("close")
      return eventlist    
    
########################################################  
symbol = 'AAPL'
data = {}
responce = fetchStockData(symbol)
#print(data)

data["Timestamp"] = parseTimestamp(responce)
data["Values"] = parseValues(responce)
data["Events"] = attachEvents(responce)
df = pd.DataFrame(data)
#print(df)

engine = create_engine('mysql://root:codio@localhost/stock_data')
df.to_sql('stocks', con=engine, if_exists='replace', index=False)
