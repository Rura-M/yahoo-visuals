import requests
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine
import os

matplotlib.interactive(True)


def menu():
    print('''
     This program displays how stock prices vary. Please choose an option:
      0. Exit
      1. Create Database
      2. Update Database
      3. Line Plot
      4. Boxplot
      5. Histogram
    ''')


def fetchStockData(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"
    headers = {
        'x-rapidapi-key': "4b9c386372msh305d0f5e33cb633p1cee26jsn477776e57ef8",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    querystring = {
        "region": "US", "symbol": symbol, "interval": "1d",
        "range": "3mo"}
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
    valueList.extend(
        inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
    valueList.extend(inputdata["chart"]["result"][0]
                     ["indicators"]["quote"][0]["close"])
    return valueList


def attachEvents(inputdata):
    eventlist = []
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("open")
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("close")
    return eventlist


def create_database(df):
    engine = create_engine('mysql://root:codio@localhost/stock_data')
    df.to_sql('stocks', con=engine, if_exists='replace', index=False)
    os.system("mysqldump -u root -pcodio stock_data > stock-file.sql")


def update_database(df):
    engine = create_engine('mysql://root:codio@localhost/stock_data')
    df.to_sql('stocks', con=engine, if_exists='append', index=False)
    os.system("mysqldump -u root -pcodio stock_data > stock-file.sql")


def line_plot(df):
    df.plot(kind='line', x='Timestamp', y='Values', color='red')
    plt.title('Variation of stock price over time')
    plt.ylabel('Values')
    plt.xlabel('Time')
    plt.show()


def boxplot(df):
    df.boxplot(column=['Values'])
    plt.title('Boxplot of values')


def histogram(df):
    df.hist(column='Values', grid=False)
    plt.title('Histogram of Stock Prices')


def handle_option(option):
    try:
        return int(option)
    except BaseException:
        return -1


# MAIN
symbol = 'AAPL'
data = {}
response = fetchStockData(symbol)
# print(data)

data["Timestamp"] = parseTimestamp(response)
data["Values"] = parseValues(response)
data["Events"] = attachEvents(response)
df = pd.DataFrame(data)
# print(df)

menu()
try:
    option = handle_option(input('Enter option:'))
except BaseException:
    print(f'Please enter input')

while option != 0:
    if option == 1:
        print('EXISTING FILE WILL BE OVERWRITTEN')
        print('Are you sure you want to continue? (y/n)')
        choice = input()
        if choice == 'y':
            create_database(df)
        else:
            continue
    elif option == 2:
        update_database(df)
    elif option == 3:
        line_plot(df)
    elif option == 4:
        boxplot(df)
    elif option == 5:
        histogram(df)
    else:
        print('\nInvalid choice, select another option')
    menu()
    option = handle_option(input('Enter your option: '))

# Data visualizaztions
# https://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot
