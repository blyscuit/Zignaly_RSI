'''
Zignaly RSI
2021 - Bliss

Buy BTC dip based on hourly RSI

'''
import math
import time
import numpy as np
from datetime import datetime
import pprint
from dotenv import load_dotenv
import os
import requests as requests
import time
import traceback

from random import randint

load_dotenv()

# set keys
zignaly_key = os.getenv("zignaly_key")
tap_key = os.getenv("tap_key")

threadhold = float(os.getenv("zig_buy_thread", '20'))
sellThreadhold = 58
buyDelay = 3600

def checkAndBuy(timer = 0, selling = False, boughtAt = 1000000000):
    if timer > time.time():
        trend_r = requests.get('https://api.taapi.io/supertrend?secret='+tap_key+'&exchange=binance&symbol=BTC/USDT&interval=15m&backtrack=2')
        print(trend_r.json())
        return (timer, selling, boughtAt)
    rsi_r = requests.get("https://api.taapi.io/rsi?secret="+tap_key+"&exchange=binance&symbol=BTC/USDT&interval=15m&backtracks=7&optInTimePeriod=12")
    # rsi_r = requests.get("https://api.taapi.io/rsi?secret="+tap_key+"&exchange=binance&symbol=BTC/USDT&interval=1h&backtracks=2")
    rsi = rsi_r.json()
    try:
        # print(rsi[0])
        rsi_all = list(map(lambda x: x['value'], rsi))
        # print(rsi_all)
        # print(min(rsi_all))
        # print(rsi[0] == min(rsi_all))
        currentRSI = rsi[0]['value']
        # if selling and currentRSI == max(rsi_all) and currentRSI >= sellThreadhold:
        if selling == True and rsi[0]['value'] >= sellThreadhold:

            coinbase_r = requests.get("https://api.coincap.io/v2/assets/bitcoin")
            coinbase = coinbase_r.json()
            currentPrice = float(coinbase["data"]["priceUsd"])
            # print('current:' + str(currentPrice) + ' bought:' + str(boughtAt) + ' execute:' + str(currentPrice > boughtAt))
            # if currentPrice > boughtAt:
            #     zig_r = requests.get('https://zignaly.com/api/signals.php?key='+zignaly_key+'&pair=BTCUSDT&type=exit&exchange=binance&signalId=1111')
            #     print('sell:' + str(rsi[0]['value']) + ' ' + str(currentPrice))
            #     return (0, False, 0)
            return (0, False, 0)

        # elif currentRSI == min(rsi_all) and currentRSI <= threadhold:
        elif selling == False and rsi[0]['value'] <= threadhold:
            coinbase_r = requests.get("https://api.coincap.io/v2/assets/bitcoin")
            coinbase = coinbase_r.json()
            currentPrice = float(coinbase["data"]["priceUsd"])
            num1= randint(111111111,99999999999)
            zig_r = requests.get('https://zignaly.com/api/signals.php?key='+zignaly_key+'&pair=BTCUSDT&type=entry&exchange=binance&positionSizePercentage=10&signalId='+str(num1)+'&limitPrice='+str(currentPrice)+'&buyTTL=7200&DCAAmountPercentage1=50&DCATargetPercentage1=-3&orderType=limit&takeProfitAmountPercentage1=100&takeProfitPercentage1=2&trailingStopDistancePercentage=-0.5&trailingStopTriggerPercentage=1')
            print('buy:' + str(rsi[0]['value']) + ' ' + str(currentPrice))            
            return (time.time() + buyDelay, True, currentPrice)
        else:
            # print(rsi[0]['value'])
            return (0, selling, boughtAt)
    except Exception as error:
        traceback.print_exc()
        return (0, selling, boughtAt)
    return (0, selling, boughtAt)

# checkAndBuy()