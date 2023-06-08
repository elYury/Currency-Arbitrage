import time
from datetime import datetime

#import symbols and calc liquidity
from func_bybit import get_bybit_symbols
from order_book_calc import orderbook_info


#import tickers
from func_bybit import get_bybit_ticker
from func_kucoin import get_kucoin_ticker
from func_gateio import get_gateio_ticker
from func_hitbtc import get_hitbtc_ticker
from func_bitmart import get_bitmart_ticker

import json

#import all the symbols from json file
from sym_list import sym_list
key = sym_list
#with open('sym_list.json') as json_file:
    #key = json.load(json_file)

#initialize values
#minimum % difference for arbitrage
minimum_gain = 20

#counting success (s) and failiure of abri opportunities
count = 0
scount = 0

#create a list of dicitonaries "yes im doing it manually because its easier" ctl c is king
megalist = []
exchange_list = []

megalist.append(get_bybit_ticker())
exchange_list.append("Bybit")

megalist.append(get_kucoin_ticker())
exchange_list.append("Kucoin")

megalist.append(get_gateio_ticker())
exchange_list.append("Gate.io")

megalist.append(get_hitbtc_ticker())
exchange_list.append("Hitbtc")

megalist.append(get_bitmart_ticker())
exchange_list.append("Bitmart")

print('')

#time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")


# calculation looping over each key on each exchange
for x in range(len(key)):
    current_key = key[x]
    for i in range(len(megalist)):
        for j in range(len(megalist)):
            #if same exchange is getting compared agaisnt itself then skip
            if i == j:
                continue
            #try to look at the price, but if one cant be sourced then skip
            try:
                ex1 = float(megalist[i][current_key])
                ex2 = float(megalist[j][current_key])
            except:
                continue
            # calc %
            if ex1 > ex2:
                x = ex1/ex2 * 100 - 100
                if x > minimum_gain:  
                    orderinfo = orderbook_info(current_key, exchange_list[i], exchange_list[j])
                    volume = orderinfo['volume']
                    avgprice = orderinfo['avgprice']
                    currency_base = current_key.replace("USDT","")

                    print(f"Arbitrage found {current_time}")
                    print(f"Gain: {round(x, 2)}% Pair: {current_key}")
                    print(f"BUY at {exchange_list[j]}")
                    print(f"SELL at {exchange_list[i]}")
                    print(f"Volume: {volume} {currency_base} || Average price: {avgprice} USDT")
                    print('-' * 25)
                    print()

                    scount += 1
                else:
                    count += 1

        
print(f"Arbi Opportunities: {scount}")
print(f"Unsuccesfull Arbies: {count}")
print('*Indian accent* Listen, Average price might not be accurate, contact uncle Rakesh')
print('')
