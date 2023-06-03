import ccxt
import pandas as pd

def main():
    for exchange in ccxt.exchanges:
        try:
            print(get_price(exchange,'BTC/USDT'))
        except:
            print('failed to load price')

    
def get_price(exchange, symbol):
    inst = getattr(ccxt, exchange)()
    coin_ticker = inst.fetch_ticker(symbol)
    latest_price = (float(coin_ticker['info']['ask']) + float(coin_ticker['info']['bid'])) / 2
    return latest_price


main()