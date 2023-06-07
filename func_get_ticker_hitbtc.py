import requests

r = requests.get("https://api.hitbtc.com/api/3/public/symbol")
r1 = requests.get("https://api.hitbtc.com/api/3/public/ticker")


def get_hitbtc_symbols():
    info = r.json()

    sym_list = []

    for key in info:
        if info[key]['quote_currency'] == 'USDT' and info[key]['status'] == 'working':
            sym_list.append(key)
        
    return sym_list

def get_hitbtc_ticker():
    ticker_list = []
    sym_list = get_hitbtc_symbols()
    ticker = r1.json()

    for i in range(len(sym_list)):
        for key in ticker:
            if sym_list[i] == key:
                symbol = sym_list[i]
                symbol_ticker = {symbol: ticker[key]['last']}
                ticker_list.append(symbol_ticker)
                
    sorteddict = {}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict

#print(get_hitbtc_ticker())