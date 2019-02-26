# robo_advisor.py

from dotenv import load_dotenv
import json
import os
import requests
import sys
import csv
import pandas
import datetime

load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

#Registers api key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

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

#Creates json file for chosen ticker using requests.get and validates that ticker request was successful
alphavantage_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+ticker_symbol+'&outputsize=compact&apikey='+api_key)
if "Error" in alphavantage_data.text:
    print("-----------------------------------------------------")
    print("Sorry, but we couldn't find any data for the selected ticker.")
    sys.exit("Please re-run the program and try again!")
else:
    print("Downloading data...")
    print("-----------------------------------------------------")

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
latest_close = float(pandas_data['Closing Price'][0])
average_close = mean(pandas_data['Closing Price'].astype(float))
rate_close = (float(pandas_data['Closing Price'][0]) - float(pandas_data['Closing Price'][4])) / 5
latest_date = pandas_data['Date'][0]

#Determine recommendation
recommendation = "null"
reasoning = "null"
if latest_close > average_close:
    recommendation = "Do not buy"
    reasoning = "The most recent closing price is greater than the average over the past 100 trading days, so you should wait for the price to drop."
else:
    if rate_close > 0:
        recommendation = "Buy"
        reasoning = "The most recent closing price is lower than the average but has increased over the last five days, so you should buy until the price decreases again."
    else:
        recommendation = "Do not buy"
        reasoning = "The stock price has been decreasing and is below the average closing price over the last 100 trading days, so you may want to wait until the price starts increasing."

print("-----------------------------------------------------")
print(f"STOCK SYMBOL: {ticker_symbol}")
print("RUN AT: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("-----------------------------------------------------")
print("LATEST DAY OF AVAILABLE DATA: "+latest_date)
print("LATEST DAILY CLOSING PRICE: ${0:,.2f}".format(latest_close))
print("RECENT HIGH: ${0:,.2f}".format(recent_max))
print("RECENT LOW: ${0:,.2f}".format(recent_min))
print("-----------------------------------------------------")
print("RECOMMENDATION: "+recommendation)
print("RECOMMENDATION REASON: "+reasoning)
print("-----------------------------------------------------")
