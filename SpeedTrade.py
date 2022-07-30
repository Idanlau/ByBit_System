from pybit.spot import HTTP
import pandas as pd
import talib
import numpy as np
import math
from datetime import datetime
from datetime import timedelta



def buy(coin):
    print(session.place_active_order(
        symbol=str(coin),
        side="Buy",
        type="MARKET",
        qty=10,
        timeInForce="GTC"
    ))

def sell(qty):
    print(session.place_active_order(
        symbol="ETHUSDT",
        side="Sell",
        type="MARKET",
        qty=qty,
        timeInForce="GTC"
    ))


# session = HTTP("https://api.bybit.com",
#                api_key="", api_secret="",
#          )

session = HTTP("https://api-testnet.bybit.com",
               api_key="nFCs0FSv5d4Q2DikrV", api_secret="DvN3XSSbYgn8bPyu66VlZ6D5fWSwyOjcdnag",
         )

# cryptos = {"BTCUSDT":[], "ETHUSDT":[],"MATICUSDT":[],"AVAXUSDT":[],"ADAUSDT":[]}

cryptos = {"BTCUSDT":[], "ETHUSDT":[]}


inital_count = 24

for pair in cryptos.keys():
    data = session.query_kline(
        symbol=pair,
        interval="1h",
        limit=100,
    )

    high = []
    low = []
    close = []
    potential_buys = []

    #print(pair)

    for i in data['result']:
        high.append(i[2])
        low.append(i[3])
        close.append(i[4]) #4th element from the data['result'] is closing price

    d = {'high':high,'low':low,'close':close}

    df = pd.DataFrame(data = d)

    macd, signal, hist = talib.MACD(df['close'], fastperiod = 12, slowperiod = 26, signalperiod = 9)


    first = True
    macd_h = None #macd higher
    signal_h = None #signal higher


    today = datetime.date(datetime.now())
    yesterday = today - timedelta(days=1)

    count = inital_count

    rsi = talib.RSI(df['close'], timeperiod = 14)
    last_rsi = rsi.iloc[-1]

    if (last_rsi <= 30):
        cryptos[pair].append("BUY NOW, Oversold")
    elif last_rsi >= 70:
        cryptos[pair].append("SELL NOW, Overbought")

    real = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)

    cryptos[pair].append(last_rsi) #Need to write comments


min_rsi = 1000
coin = None

for key,value in cryptos.items():
    if value[0] <= 30 and value[0] < min_rsi:
        coin = key



balance = session.get_wallet_balance()

print(cryptos)

for i in balance['result']['balances']:
    print(str(i['coin']) + ":" + str(i['free']))



if coin != None:
    buy(coin)

# sell()

