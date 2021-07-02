import requests

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
    
########################################################  
symbol = 'AAPL'

data = fetchStockData(symbol)
print(data)
