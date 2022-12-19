import asyncio
from websockets import connect
import aiofiles
import sys
import json
import httpx
from datetime import datetime
#import heikenAshiBuilder
# to do: fetch list of markets and update automatically with new additions
#pairs_list = ['10000NFTUSDT','1000BTTUSDT','1000LUNCUSDT','1000XECUSDT','1INCHUSDT','AAVEUSDT','ACHUSDT','ADAUSD','ADAUSDT','AGLDUSDT','AKROUSDT','ALGOUSDT','ALICEUSDT','ALPHAUSDT','ANCUSDT','ANKRUSDT','ANTUSDT','APEUSDT','API3USDT','APTUSDT','ARPAUSDT','ARUSDT','ASTRUSDT','ATOMUSDT','AUDIOUSDT','AVAXUSDT','AXSUSDT','BAKEUSDT','BALUSDT','BANDUSDT','BATUSDT','BCHUSDT','BELUSDT','BICOUSDT','BITUSD','BITUSDT','BLZUSDT','BNBUSDT','BNXUSDT','BOBAUSDT','BSVUSDT','BSWUSDT','BTCUSD','BTCUSDH22','BTCUSDH23','BTCUSDM22','BTCUSDT','BTCUSDU21','BTCUSDU22','BTCUSDZ21','BTCUSDZ22','BTTUSDT','C98USDT','CEEKUSDT','CELOUSDT','CELRUSDT','CHRUSDT','CHZUSDT','CKBUSDT','COMPUSDT','COTIUSDT','CREAMUSDT','CROUSDT','CRVUSDT','CTCUSDT','CTKUSDT','CTSIUSDT','CVCUSDT','CVXUSDT','DARUSDT','DASHUSDT','DENTUSDT','DGBUSDT','DODOUSDT','DOGEUSDT','DOTUSD','DOTUSDT','DUSKUSDT','DYDXUSDT','EGLDUSDT','ENJUSDT','ENSUSDT','EOSUSD','EOSUSDT','ETCUSDT','ETHUSD','ETHUSDH22','ETHUSDH23','ETHUSDM22','ETHUSDT','ETHUSDU21','ETHUSDU22','ETHUSDZ21','ETHUSDZ22','ETHWUSDT','FILUSDT','FITFIUSDT','FLMUSDT','FLOWUSDT','FTMUSDT','FTTUSDT','FXSUSDT','GALAUSDT','GALUSDT','GLMRUSDT','GMTUSDT','GMXUSDT','GRTUSDT','GSTUSDT','GTCUSDT','HBARUSDT','HNTUSDT','HOTUSDT','ICPUSDT','ICXUSDT','ILVUSDT','IMXUSDT','INJUSDT','IOSTUSDT','IOTAUSDT','IOTXUSDT','JASMYUSDT','JSTUSDT','KAVAUSDT','KDAUSDT','KEEPUSDT','KLAYUSDT','KNCUSDT','KSMUSDT','LDOUSDT','LINAUSDT','LINKUSDT','LITUSDT','LOOKSUSDT','LPTUSDT','LRCUSDT','LTCUSD','LTCUSDT','LUNA2USDT','LUNAUSD','LUNAUSDT','MANAUSD','MANAUSDT','MASKUSDT','MATICUSDT','MINAUSDT','MKRUSDT','MTLUSDT','NEARUSDT','NEOUSDT','OCEANUSDT','OGNUSDT','OMGUSDT','ONEUSDT','ONTUSDT','OPUSDT','PAXGUSDT','PEOPLEUSDT','QTUMUSDT','RAYUSDT','REEFUSDT','RENUSDT','REQUSDT','RNDRUSDT','ROSEUSDT','RSRUSDT','RSS3USDT','RUNEUSDT','RVNUSDT','SANDUSDT','SCRTUSDT','SCUSDT','SFPUSDT','SHIB1000USDT','SKLUSDT','SLPUSDT','SNXUSDT','SOLUSD','SOLUSDT','SPELLUSDT','SRMUSDT','STGUSDT','STMXUSDT','STORJUSDT','STXUSDT','SUNUSDT','SUSHIUSDT','SWEATUSDT','SXPUSDT','THETAUSDT','TLMUSDT','TOMOUSDT','TRBUSDT','TRXUSDT','TWTUSDT','UNFIUSDT','UNIUSDT','USDCUSDT','USTUSDT','VETUSDT','WAVESUSDT','WOOUSDT','XCNUSDT','XEMUSDT','XLMUSDT','XMRUSDT','XNOUSDT','XRPUSD','XRPUSDT','XTZUSDT','YFIUSDT','YGGUSDT','ZECUSDT','ZENUSDT','ZILUSDT','ZRXUSDT']

default_pair = "SOLUSDT"

async def orderbook_download(pair):
    #pair_lower = pair.lower()
    url = 'wss://stream.bybit.com/contract/usdt/public/v3'
    today = datetime.now().date()

    async with connect(url, ping_interval=None) as websocket:
        args = '{"op": "subscribe", "args": ["kline.15.' + str(pair) + '"]}'
        await websocket.send(args)

        while True:
            data_rcv_strjson = await websocket.recv();
            #print(data_rcv_strjson)
            data_rcv_strjson =  json.loads(data_rcv_strjson)
            print(data_rcv_strjson)
            if (not data_rcv_strjson.__contains__('data')):
                continue
            for i in range(len(data_rcv_strjson['data'])):
                if (data_rcv_strjson['data'][i]['confirm'] == True):
                    async with aiofiles.open(f'{pair}-klines-{today}.txt', mode = 'a') as f:
                        await f.write(json.dumps(data_rcv_strjson['data'][i]) + "\n")

                
    pass
asyncio.run(orderbook_download(default_pair))
#for pair in pairs_list:
#    print(pair)
#    asyncio.run(orderbook_download(pair))

