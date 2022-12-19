import tradeBot
import heikenAshiBuilder

def test():
    pair = "SOLUSDT"
    klines = tradeBot.getKlines(symbol=pair)
    print(klines)
    payload = []
    for i in klines:
        kline = {}
        kline["open"] = float(i[1])
        kline["high"] = float(i[2])
        kline["low"] = float(i[3])
        kline["close"] = float(i[4])
        payload.append(kline)
    payload.reverse()
    heikenAshiBuilder.captureKlines(payload, pair=pair)
    pass

test()