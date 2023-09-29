# Dont be judgy we all have written spaggetti code, it gets the job done. But need quality of life improvments.
from func_bybit import get_bybit_symbols
from func_kucoin import get_kucoin_symbols
from func_gateio import get_gateio_symbols
from func_hitbtc import get_hitbtc_symbols
from func_bitmart import get_bitmart_symbols

from func_binance import get_binance_symbols
from func_cexio import get_cexio_symbols
from func_hotcoinglobal import get_hotcoinglobal_symbols
from func_kraken import get_kraken_symbols
from func_okx import get_okx_symbols

bybit = get_bybit_symbols()
kucoin = get_kucoin_symbols()
gateio = get_gateio_symbols()
hitbtc = get_hitbtc_symbols()
bitmart = get_bitmart_symbols()

binance = get_bitmart_symbols()
cexio = get_bitmart_symbols()
hotcoinglobal = get_bitmart_symbols()
kraken = get_bitmart_symbols()
okx = get_bitmart_symbols()

total_sym_list = bybit + kucoin + gateio + hitbtc + bitmart + binance + cexio + hotcoinglobal + kraken + okx

#print(sym_list)
x = '_'
y = '-'
n1 = '1'
n2 = '2'
n3 = '3'
n4 = '4'
n5 = '5'
n6 = '6'
n7 = '7'
n8 = '8'
n9 = '9'
n10 = "PERP"
n11 = "$"

for i in range(len(total_sym_list)):
    try:
        current_string = total_sym_list[i]
        if x in current_string:
            total_sym_list[i] = current_string.replace("_", "")
        if y in current_string:
            total_sym_list[i] = current_string.replace("-", "")
        if n1 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT") #trust me
        if n2 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n3 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n4 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n5 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n6 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n7 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n8 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n9 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n10 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
        if n11 in current_string:
            total_sym_list[i] = current_string.replace(current_string, "BTCUSDT")
    except:
        break

#here we get rid of the extra BTCUSDT
merged_sym_list = list(set(total_sym_list))
sorted_list = sorted(merged_sym_list)
print(sorted_list)
