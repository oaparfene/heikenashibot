from config import session, ws, api_key, api_secret
import time
import hmac
import hashlib
import requests
import uuid
import json

#httpClient = requests.Session()
recv_window = str(10000)
#url = 'https://api.bybit.com'

def getBalance():
    url = 'https://api.bybit.com/contract/v3/private/account/wallet/balance' #get wallet balance
    timestamp = int(time.time())* 1000
    param_str = f'{timestamp}{api_key}{recv_window}'#category=option&symbol=BTC-29JUL22-25000-C'

    byte_key = bytes(api_secret, 'UTF-8')
    msg = param_str.encode()

    h = hmac.new( byte_key, msg, hashlib.sha256).hexdigest()

    headers = {
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-SIGN': f'{h}',
        'X-BAPI-API-KEY': f'{api_key}',
        'X-BAPI-TIMESTAMP': str(timestamp),
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json',
    }

    data = requests.get(url, headers = headers)
    data = data.json()
    assetList = data['result']['list']
    for i in range(len(assetList)):
        if (assetList[i]['coin'] == 'USDT'):
            print(assetList[i])
            return float(assetList[i]['walletBalance'])

def getPairPrice(pair):
    url = f'https://api.bybit.com/derivatives/v3/public/tickers?category=linear&symbol={pair}'
    data = requests.get(url)
    data = data.json()
    data = data['result']['list'][0]['lastPrice']
    print(data)

def cancelAllOrders():
    url = 'https://api.bybit.com/contract/v3/private/order/cancel-all'
    timestamp = int(time.time())* 1000
    param_str = f'{timestamp}{api_key}{recv_window}'

    body = {
        "settleCoin": "USDT"
    }

    param_str = param_str + json.dumps(body)
    byte_key = bytes(api_secret, 'UTF-8')
    msg = param_str.encode()

    h = hmac.new( byte_key, msg, hashlib.sha256).hexdigest()

    headers = {
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-SIGN': f'{h}',
        'X-BAPI-API-KEY': f'{api_key}',
        'X-BAPI-TIMESTAMP': str(timestamp),
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json',
    }

    data = requests.post(url, headers = headers, json = body)
    data = data.json()
    print (data)

def getPosition():
    url = 'https://api.bybit.com/contract/v3/private/position/list?settleCoin=USDT&dataFilter=valid'
    timestamp = int(time.time())* 1000
    param_str = f'{timestamp}{api_key}{recv_window}settleCoin=USDT&dataFilter=valid'

    byte_key = bytes(api_secret, 'UTF-8')
    msg = param_str.encode()

    h = hmac.new( byte_key, msg, hashlib.sha256).hexdigest()

    headers = {
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-SIGN': f'{h}',
        'X-BAPI-API-KEY': f'{api_key}',
        'X-BAPI-TIMESTAMP': str(timestamp),
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json',
    }

    data = requests.get(url, headers = headers)
    data = data.json()
    print(data)
    return data['result']['list']

def closeAllPositions():
    positions = getPosition()
    for i in positions:
        print(i)

        url = 'https://api.bybit.com/contract/v3/private/order/create' #create private order
        timestamp = int(time.time())* 1000
        param_str = f'{timestamp}{api_key}{recv_window}'

        body = {
        "symbol": f"{i['symbol']}",
        "side": f"{'Sell' if i['side']=='Buy' else 'Buy'}",
        "positionIdx": 0,
        "orderType": "Market",
        "qty": f"{float(i['size'])}",
        "timeInForce": "GoodTillCancel",
        "reduce_only": "true",
        }

        param_str = param_str + json.dumps(body)
        byte_key = bytes(api_secret, 'UTF-8')
        msg = param_str.encode()

        h = hmac.new( byte_key, msg, hashlib.sha256).hexdigest()

        headers = {
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-SIGN': f'{h}',
            'X-BAPI-API-KEY': f'{api_key}',
            'X-BAPI-TIMESTAMP': str(timestamp),
            'X-BAPI-RECV-WINDOW': recv_window,
            'Content-Type': 'application/json',
        }
        print(body)
        data = requests.post(url, headers = headers, json=body)
        data = data.json()
        print (data)




def placeOrder(side, order_type, pair, quantity, tp, sl):
    url = 'https://api.bybit.com/contract/v3/private/order/create' #create private order
    timestamp = int(time.time())* 1000
    param_str = f'{timestamp}{api_key}{recv_window}'
    body = {}
    if (order_type == 'Market'):
        body = {
        "symbol": f"{pair}",
        "side": f"{side}",
        "positionIdx": 1 if side=='Buy' else 2,
        "orderType": "Market",
        "qty": f"{quantity}",
        "timeInForce": "GoodTillCancel",
        "takeProfit": f"{tp}",
        "stopLoss": f"{sl}",
        }
    elif (order_type == 'Limit'):
        # todo: finish this up
        body = {
        "symbol": f"{pair}",
        "side": f"{side}",
        "positionIdx": 1,
        "orderType": "Limit",
        "qty": f"{quantity}",
        "price": "12",
        "triggerDirection": 2,
        "triggerPrice": "12",
        "triggerBy": "MarkPrice",
        "timeInForce": "GoodTillCancel",
        "orderLinkId": "a004",
        "takeProfit": "13",
        "stopLoss": "11",
        "reduce_only": 'false',
        "closeOnTrigger": 'false'
        }

    param_str = param_str + json.dumps(body)
    byte_key = bytes(api_secret, 'UTF-8')
    msg = param_str.encode()

    h = hmac.new( byte_key, msg, hashlib.sha256).hexdigest()

    headers = {
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-SIGN': f'{h}',
        'X-BAPI-API-KEY': f'{api_key}',
        'X-BAPI-TIMESTAMP': str(timestamp),
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json',
    }
    
    data = requests.post(url, headers = headers, json=body)
    data = data.json()
    print (data)

def getKlines(symbol, interval=15, lookback=10):
    url = 'https://api.bybit.com/derivatives/v3/public/kline' #create private order
    timestamp = int(time.time())* 1000
    start_timestamp = timestamp - (interval*60*1000*(lookback))

    url=url + f"?category=linear&symbol={symbol}&interval={interval}&start={start_timestamp}&end={timestamp}"
    
    data = requests.get(url)
    data = data.json()
    #print(data)
    #print(len(data['result']['list']))
    return data['result']['list']




getKlines(symbol="SOLUSDT")
#placeOrder('Buy', 'Limit', 'SOLUSDT', 1, 15, 11)
#closeAllPositions()
#getBalance()
#cancelAllOrders()