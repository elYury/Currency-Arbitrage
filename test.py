import time
from func_get_ticker_bybit import get_bybit_ticker
from func_get_ticker_bybit import get_sym_list
from func_get_ticker_kucoin import get_kucoin_ticker

key = get_sym_list()
bybitticker = get_bybit_ticker()
kucointicker = get_kucoin_ticker()





for i in range(len(kucointicker)):
    x = kucointicker[i].keys()
    if x.__contains__('USDT') == True:

        print(x)