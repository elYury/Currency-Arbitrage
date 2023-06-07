import ccxt
import pandas as pd

def main():
    count_loaded = 0
    count_failed = 0
    for exchange in ccxt.exchanges:
        try:
            print(get_price(exchange,'BTC/USDT'))
            count_loaded += 1
        except:
            print('failed to load price')
            count_failed += 1
    print(f"exchanges loaded: {count_loaded}")
    print(f"exchanges failed to load: {count_failed}")
    
def get_price(exchange, symbol):
    inst = getattr(ccxt, exchange)()
    coin_ticker = inst.fetch_ticker(symbol)
    latest_price = (float(coin_ticker['info']['ask']) + float(coin_ticker['info']['bid'])) / 2
    return latest_price


main()