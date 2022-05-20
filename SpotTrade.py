from pybit.spot import HTTP
import pandas as pd
import talib
import numpy as np
import math
from datetime import datetime
from datetime import timedelta


session = HTTP("https://api.bybit.com",
               api_key="", api_secret="",
         )


cryptos = {"BTCUSDT":[], "ETHUSDT":[], "XRPUSDT":[], "EOSUSDT":[],
           "DOTUSDT":[], "XLMUSDT":[], "LTCUSDT":[], "DOGEUSDT":[], "BITUSDT":[], "CHZUSDT":[],
           "AXSUSDT":[],"MANAUSDT":[],"DYDXUSDT":[],"MKRUSDT":[],"COMPUSDT":[],"AAVEUSDT":[],
           "YFIUSDT":[],"LINKUSDT":[],"SUSHIUSDT":[],"UNIUSDT":[],"KSMUSDT":[],"ICPUSDT":[],"ADAUSDT":[],
           "KLAYUSDT":[],"XTZUSDT":[],"BCHUSDT":[],"SRMUSDT":[],"QNTUSDT":[],"GRTUSDT":[],
           "SOLUSDT":[],"FILUSDT":[],"OMGUSDT":[],"TRIBEUSDT":[],"BATUSDT":[],"ZRXUSDT":[],
           "CRVUSDT":[],"AGLDUSDT":[],"ANKRUSDT":[],"PERPUSDT":[],"MATICUSDT":[],"WAVESUSDT":[],"LUNAUSDT":[],
           "DASHUSDT":[],"SPELLUSDT":[],"SHIBUSDT":[],"FTMUSDT":[],"ATOMUSDT":[],"ALGOUSDT":[],"ENJUSDT":[],
           "CBXUSDT":[],"SANDUSDT":[],"AVAXUSDT":[],"WOOUSDT":[],"FTTUSDT":[],"GODSUSDT":[],"IMXUSDT":[],
           "ENSUSDT":[],"GMUSDT":[],"CWARUSDT":[],"CAKEUSDT":[],"STETHUSDT":[],"GALUSDT":[],"LFWUSDT":[],
           "SLPUSDT":[],"C98USDT":[],"PSPUSDT":[],"GENEUSDT":[],"AVAUSDT":[],"ONEUSDT":[],"PTUUSDT":[],
           "SHILLUSDT":[],"XYMUSDT":[],"BOBAUSDT":[],"INSURUSDT":[],"JASMYUSDT":[],"GALAUSDT":[],
           "RNDRUSDT":[],"TRVLUSDT":[],"WEMIXUSDT":[],"XEMUSDT":[],"KMAUSDT":[],"BICOUSDT":[],
           "CELUSDT":[],"UMAUSDT":[],"HOTUSDT":[],"NEXOUSDT":[],"AMPUSDT":[],"BNTUSDT":[],"SNXUSDT":[],
           "RENUSDT":[],"1INCHUSDT":[],"TELUSDT":[],"SISUSDT":[],"LRCUSDT":[],"LDOUSDT":[],"REALUSDT":[],
           "KRLUSDT":[],"DEVTUSDT":[],"CRAFTUSDT":[],"1SOLUSDT":[],"PLTUSDT":[],"IZIUSDT":[],"QTUMUSDT":[],
           "DCRUSDT":[],"ZENUSDT":[],"THETAUSDT":[],"MXUSDT":[],"DGBUSDT":[],"RVNUSDT":[],"EGLDUSDT":[],
           "RUNEUSDT":[],"DFLUSDT":[],"RAINUSDT":[],"RUNUSDT":[],"XECUSDT":[],"ZECUSDT":[],"ICXUSDT":[],
           "XDCUSDT":[],"HNTUSDT":[],"BTGUSDT":[],"ZILUSDT":[],"HBARUSDT":[],"FLOWUSDT":[],"SOSUSDT":[],
           "KASTAUSDT":[],"GASUSDT":[],"STXUSDT":[],"SIDUSUSDT":[],"VPADUSDT":[],"GGMUSDT":[],
           "LOOKSUSDT":[],"MBSUSDT":[],"DAIUSDT":[],"BUSDUSDT":[],"ACAUSDT":[],"MVUSDT":[],"MIXUSDT":[],
           "RSS3USDT":[],"SYNRUSDT":[],"TAPUSDT":[],"ERTHAUSDT":[],"GMXUSDT":[],"POSIUSDT":[],"TUSDT":[],
           "ACHUSDT":[],"JSTUSDT":[],"SUNUSDT":[],"BTTUSDT":[],"TRXUSDT":[],"NFTUSDT":[],"POKTUSDT":[],
           "SCRTUSDT":[],"PSTAKEUSDT":[],"SONUSDT":[],"HEROUSDT":[],"DOMEUSDT":[],"ZBCUSDT":[],"USTUSDT":[],
           "BNBUSDT":[],"NEARUSDT":[],"PAXGUSDT":[],"SDUSDT":[],"APEUSDT":[],"FIDAUSDT":[],"MINAUSDT":[],
           "SCUSDT":[],"RACAUSDT":[],"IMEUSDT":[],"CAPSUSDT":[],"STGUSDT":[],"LMRUSDT":[]}


inital_count = int(input("How many periods do you want to look back for significant data? "))

for pair in cryptos.keys():
    data = session.query_kline(
        symbol=pair,
        interval="1h",
        limit=100,
    )

    high = []
    low = []
    close = []

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

    try:
        for i in range (len(macd)-inital_count,len(macd)-1):

            if math.isnan(macd[i]) == False and math.isnan(signal[i]) == False:

                if first == True:
                    if macd[i] > signal[i]:
                        macd_h = True
                        signal_h = False
                        first = False

                    elif macd[i] < signal[i]:
                        macd_h = False
                        signal_h = True
                        first = False
                else:
                    if macd[i] >= signal[i]:
                        if macd_h != True:
                            cryptos[pair].append(f"MACD cross above at {today - timedelta(days=99-(i))}")
                            macd_h = True
                            signal_h = False

                    if signal[i] >= macd[i]:
                        if signal_h != True:
                            cryptos[pair].append(f"MACD cross below at {today - timedelta(days=99-(i))}")
                            macd_h = False
                            signal_h = True
                count -= 1

                if count == 0:
                    break
    except KeyError:
        pass


    rsi = talib.RSI(df['close'], timeperiod = 14)
    last_rsi = rsi.iloc[-1]

    if (last_rsi <= 30):
        cryptos[pair].append("BUY NOW, Oversold")
    elif last_rsi >= 70:
        cryptos[pair].append("SELL NOW, Overbought")

    real = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
    # print(pd.to_numeric(real.iloc[-1]))
    #
    # print(pd.to_numeric(real.iloc[-1])/pd.to_numeric(df['close'].iloc[-1]))

    cryptos[pair].append(pd.to_numeric(real.iloc[-1])/pd.to_numeric(df['close'].iloc[-1])) #Need to write comments


for key,value in cryptos.items():
    print(key,value)
# for i in session.query_symbol()['result']:
#     print(i['name'])
