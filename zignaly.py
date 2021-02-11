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

load_dotenv()

# set keys
zignaly_key = os.getenv("zignaly_key")
tap_key = os.getenv("tap_key")

threadhold = 25
sellThreadhold = 61
buyDelay = 3600

def checkAndBuy(timer = 0, selling = False):
    if timer > time.time():
        trend_r = requests.get('https://api.taapi.io/supertrend?secret='+tap_key+'&exchange=binance&symbol=BTC/USDT&interval=15m&backtrack=2')
        print(trend_r.json())
        return (timer, selling)
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
            zig_r = requests.get('https://zignaly.com/api/signals.php?key='+zignaly_key+'&pair=BTCUSDT&type=exit&exchange=binance&signalId=1111')
            print('sell:' + str(rsi[0]['value']))
            return (0, False)
        # elif currentRSI == min(rsi_all) and currentRSI <= threadhold:
        elif selling == False and rsi[0]['value'] <= threadhold:
            zig_r = requests.get('https://zignaly.com/api/signals.php?key='+zignaly_key+'&pair=BTCUSDT&type=entry&exchange=binance&positionSizePercentage=50&signalId=1111')
            print('buy:' + str(rsi[0]['value']))
            return (time.time() + buyDelay, True)
        else:
            print(rsi[0]['value'])
            return (0, selling)
    except Exception as error:
        traceback.print_exc()
        return (0, selling)

# checkAndBuy()