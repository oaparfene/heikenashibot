import plotly.graph_objects as go
import pandas as pd
#candles = []
#ha_candles = []
main_pair = ''


def captureKlines(klines, pair):
    main_pair = pair
    candles = klines
    ha_candles = calcHeikenAshi(candles)
    signal = calcSignal(ha_candles)
    print("HA")
    print(ha_candles)
    print(signal)
    dfpl = pd.DataFrame(ha_candles)
    print(dfpl)
    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                    open=dfpl['Heiken_Open'],
                    high=dfpl['Heiken_High'],
                    low=dfpl['Heiken_Low'],
                    close=dfpl['Heiken_Close'])])
    fig.show()

    #if (signal[-1] != 0):
        #initTrade(signal[-1])
        #pass

def calcHeikenAshi(candles):
    print(len(candles))
    ha_list = []
    for i in range(len(candles)):
        ha = {}
        ha['Heiken_Close'] = round((candles[i]['open'] + candles[i]['high'] + candles[i]['low'] + candles[i]['close'])/4, 3)
        ha['Heiken_Open'] = round(candles[i]['open'], 3)
        for i in range(len(ha_list)):
            ha['Heiken_Open'] = round((ha_list[i-1]['Heiken_Open'] + ha_list[i-1]['Heiken_Close'])/2, 3)
        ha['Heiken_High'] = round(max(ha['Heiken_Open'], ha['Heiken_Close'], candles[i]['high']), 3)
        ha['Heiken_Low'] = round(min(ha['Heiken_Open'], ha['Heiken_Close'], candles[i]['low']),3)
        ha_list.append(ha)
    return ha_list

def isGreen(ha_kline):
    if(ha_kline['Heiken_Open'] > ha_kline['Heiken_Close']):
        return False
    return True

def calcSignal(ha_candles):
    ordersignal=[0]*len(ha_candles)
    for i in range(1, len(ha_candles)):
        if (not isGreen(ha_candles[i]) and isGreen(ha_candles[i-1]) and not isDoji(ha_candles, i)):
            ordersignal[i]=1
        if (isGreen(ha_candles[i]) and not isGreen(ha_candles[i-1]) and not isDoji(ha_candles, i)):
            ordersignal[i]=2
    return ordersignal

def isDoji(ha_candles, i):
    if ((abs(ha_candles[i]['Heiken_Close'] - ha_candles[i]['Heiken_Open']) / ha_candles[i]['Heiken_Open']) < 0.001):
        return True
    return False

def initTrade(signal):
    if(signal == 1):
        placeOrder('sell', 'market', main_pair, quantity, tp, sl)
        pass