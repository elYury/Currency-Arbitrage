import time
from func_get_ticker_bybit import get_bybit_ticker
from func_get_ticker_bybit import get_sym_list
from func_get_ticker_kucoin import get_kucoin_ticker

key = get_sym_list()
bybitticker = get_bybit_ticker()
kucointicker = get_kucoin_ticker()

count = 0
scount = 0
# 5%
for i in range(len(key)):
    current_key = key[i]
    for j in range(len(key)):
        if bybitticker[i].keys() == kucointicker[j].keys():
            try:
                ex1 = float(bybitticker[i][current_key])
                ex2 = float(kucointicker[j][current_key])
            except:
                continue

            # calc %
            if ex1 > ex2:
                x = ex1/ex2 * 100 - 100
                if x > 3:
                    print(f"ARBI of {x}%! BUY {current_key} at KUCOIN SELL at BYBIT")
                    scount += 1
                    #print(f"BYBIT: {ex1}")
                    #print(f"KUCOIN: {ex2}")
                else:
                    count += 1
                    #print("-")
            elif ex1 < ex2:
                y = ex2/ex1 * 100 - 100
                if y > 3:
                    print(f"ARBI of {y}%! BUY {current_key} at BYBIT SELL at KUCOIN")
                    scount += 1
                    #print(f"BYBIT: {ex1}")
                    #print(f"KUCOIN: {ex2}")
                else:
                    count += 1
                    #print("-")
            else:
                count += 1
        
            
print(f"Arbi Opportunities: {scount}")
print(f"Unsuccesful Arbis: {count}")
