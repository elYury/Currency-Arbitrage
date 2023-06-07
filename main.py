import time
from datetime import datetime

#import symbols
from func_get_ticker_bybit import get_bybit_symbols

#import tickers
from func_get_ticker_bybit import get_bybit_ticker
from func_get_ticker_kucoin import get_kucoin_ticker
from func_get_ticker_gateio import get_gateio_ticker
from func_get_ticker_hitbtc import get_hitbtc_ticker
from func_get_ticker_bitmart import get_bitmart_ticker

#initialize values
    #TODO: key function needs to be changed once we have enough exchanges
key = get_bybit_symbols()

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
                if x > 20 and x < 100:
                    print(f"Arbitrage found {current_time}")
                    print(f"Gain: {round(x, 2)}% Pair: {current_key}")
                    print(f"BUY AT: {exchange_list[j]}")
                    print(f"SELL AT: {exchange_list[i]}")
                    print('-' * 25)

                    scount += 1
                else:
                    count += 1

        
print(f"Arbi Opportunities: {scount}")
print(f"Unsuccesfull Arbies: {count}")
print('')
