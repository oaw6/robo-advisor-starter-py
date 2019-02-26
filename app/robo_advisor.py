# robo_advisor.py

from dotenv import load_dotenv
import json
import os
import requests
import sys
import csv
import pandas

load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print("API KEY: " + api_key)

#Introduces the program and asks for input
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("Welcome to the Robo-Advisor Investing Recommendation")
print("Application. This app will recommend whether or not")
print("to buy any stock you are curious about.")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
ticker_symbol = input("Please type the ticker symbol of your desired stock:")
print("-----------------------------------------------------")

#Validation to make sure ticker is of the proper format
if len(ticker_symbol) > 5:
    print("Uh-oh! The maximum amount of letters for a ticker symbol is 5.")
    sys.exit("Please re-run the program and try again!")
elif ticker_symbol.isalpha():
    print("Ticker format validated.")
    print("-----------------------------------------------------")
else:
    print("Uh-oh! Remember that ticker symbols only contain letters.")
    sys.exit("Please re-run the program and try again!")

#symbol = "NFLX" # TODO: capture user input, like... input("Please specify a stock symbol: ")

#Creates json file for chosen ticker using requests.get and validates that ticker request was successful
alphavantage_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+ticker_symbol+'&outputsize=compact&apikey='+api_key)
if "Error" in alphavantage_data.text:
    print("-----------------------------------------------------")
    print("Sorry, but we couldn't find any data for the selected ticker.")
    sys.exit("Please re-run the program and try again!")
else:
    print("-----------------------------------------------------")
    print("Downloading data...")
    print("-----------------------------------------------------")
#json_data = alphavantage_data.json()

#Parse json data and create lists to hold values
json_parsed = json.loads(alphavantage_data.text)
dates = []
open_prices = []
high_prices = []
low_prices = []
close_prices = []
for key, value in json_parsed['Time Series (Daily)'].items():
    dates.append(key)
    open_prices.append(value['1. open'])
    high_prices.append(value['2. high'])
    low_prices.append(value['3. low'])
    close_prices.append(value['4. close'])

#Convert lists to csv file (with help from stack exchange)
pandas_data = pandas.DataFrame({'Date':dates,'Opening Price':open_prices, 'Daily High': high_prices,'Daily Low': low_prices,'Closing Price': close_prices})
pandas_data.to_csv('../data/'+ticker_symbol+'.csv')

#Create mean function
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

#Collect important data from data frame
recent_max = max(pandas_data['Daily High'].astype(float))
recent_min = min(pandas_data['Daily Low'].astype(float))
latest_close = pandas_data['Closing Price'][0]
average_close = mean(pandas_data['Closing Price'].astype(float))
print(average_close)
rate_close = (float(pandas_data['Closing Price'][0]) - float(pandas_data['Closing Price'][4])) / 5
print(rate_close)

# see: https://www.alphavantage.co/documentation/#daily (or a different endpoint, as desired)
# TODO: assemble the request url to get daily data for the given stock symbol...

# TODO: use the "requests" package to issue a "GET" request to the specified url, and store the JSON response in a variable...

# TODO: further parse the JSON response...

# TODO: traverse the nested response data structure to find the latest closing price and other values of interest...
#latest_price_usd = "$100,000.00"

#
# INFO OUTPUTS
#

# TODO: write response data to a CSV file

# TODO: further revise the example outputs below to reflect real information
print("-----------------")
print(f"STOCK SYMBOL: {ticker_symbol}")
print("RUN AT: 11:52pm on June 5th, 2018")
print("-----------------")
print("LATEST DAY OF AVAILABLE DATA: June 4th, 2018")
print(f"LATEST DAILY CLOSING PRICE: {latest_close}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-----------------")
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")
