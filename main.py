import requests
import json
import datetime as dt
from twilio.rest import Client

# ---------------------ALL API ENDPOINTS AND KEYS---------------------------------#
# _________________________________Stock Data api
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "API KEY"
URL = "https://www.alphavantage.co/query"
TIME_INTERVAL = "60min"
PARAMETERS = {
    "function":"TIME_SERIES_INTRADAY",
    "symbol":STOCK,
    "interval":TIME_INTERVAL,
    "apikey":API_KEY
}

# ________________________________News Catcher api
NEWS_API_KEY = "NEWS API KEY"
NEWS_API_ENDPOINT ="https://api.marketaux.com/v1/news/all"

NEWS_PARAMETER = {
    "symbols":"TSLA",
    "language":"en",
    "api_token":NEWS_API_KEY,
    "filter_entities":"true"

}

# ___________________________Twillio api
ACCOUNT_SID = "ACCOUNT SID"
AUTH_TOKEN = "AUTH TOKEN"

# -----------------------------EXTRACTING CURRENT DATE FROM DATETIME MODULE-------------------------------#
date = dt.datetime.now()
year = date.year
month = date.month
day = date.day

# ---------------------------------- EXTRACTING STOCK DATA FROM ALPHANTAGE API----------------------------------------#

response = requests.get(url=URL, params=PARAMETERS)
response.raise_for_status()
data = response.json()[f"Time Series ({TIME_INTERVAL})"]
data_list = [value for (key, value) in data.items()]

yesterday_closing_price =float( data_list[0]["4. close"])
day_before_closing_price =float(data_list[16]["4. close"])


stock_percentage = round(((yesterday_closing_price - day_before_closing_price) /day_before_closing_price) * 100)
abs_stock_percentage = abs(stock_percentage)


# # --------------------Creating a new csv file for the stock data collected---------------------------#
# with open("stock_data.json", "w") as data_file:
#     json.dump(data, data_file, indent=4)



# ------------------------DETERMINIGN IF THE CHANGE IN STOCK IS AN ICRASE OR A DECREASE IN ORDER TO DISTINGGUISH BOTH WHEN SENDING SMS------------------------#
increase_decrease = None

if stock_percentage > 0:
    increase_decrease = "🔺"
else:
    increase_decrease = "🔻"

# ----------------------------------FETCHING DATA FOR TESLA STOCKS FROM NEWS CATCHER--------------#


news_response = requests.get(url= NEWS_API_ENDPOINT, params=NEWS_PARAMETER)


# # ____________________making a json file for recently fetched news Data
# with open("news.json", "w") as file:
#     json.dump(news_response.json()["data"], file, indent = 4)


all_news = news_response.json()["data"]
news_list = [f"{STOCK}: {increase_decrease}{abs_stock_percentage}%\nHeadlines: {all_news[i]['title']}\nNews Snippet: {all_news[i]['snippet']}\nNews Link: {all_news[i]['url']}" for i in range(len(all_news))]

# OR Alternatively
# news_list = [f"Headline: {news['title']}\nNews Snippet: {news['snippet']}\nFor Full Article: {news['url']}" for news in all_news]

# ---------------------------------------SENDING SMS WHEN THERES A SIGNIFICANT CHANGE OFMY STOCK IN THE STOCK MARKTET---------------------------------------#
if abs_stock_percentage > 1:
    for news in news_list:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(body=news,
                    from_="+15673523597",
                    to='+2348062292004'
                    )
