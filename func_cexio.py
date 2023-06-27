#https://docs.plus.cex.io/#rest-public-api-calls-pairs-info

import requests

r = requests.get("https://api.plus.cex.io/rest-public/get_pairs_info")
r1 = requests.get("https://api.plus.cex.io/rest-public/get_ticker")


def get_cexio_symbols():
    info = r.json()
    info = info['data']
    sym_list = []

    for i in range(len(info)):
        if info[i]['quote'] == 'USDT':
            symbol = info[i]['base'] + '-' + info[i]['quote']
            sym_list.append(symbol)
        
    return sym_list

def get_cexio_ticker():
    ticker_list = []
    sym_list = get_cexio_symbols()
    ticker = r1.json()
    ticker = ticker['data']

    for i in range(len(sym_list)):
        for key in ticker:
            if sym_list[i] == key and float(ticker[key]["volume"]) >= 10000:
                symbol = sym_list[i].replace('-','')
                symbol_ticker = {symbol: ticker[key]['last']}
                ticker_list.append(symbol_ticker)

    # converts a list of dictionaries into a single dictionary
    sorteddict = {}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict

def get_cexio_orderbook(sym, outputask):
    if outputask == False:
        price_type = 'bids'
    else:
        price_type = 'asks'
    
    sym = sym.replace('USDT', '-USDT')
    orderbook = requests.get('https://api.plus.cex.io/rest-public/get_order_book?pair=' + sym)
    orderbook = orderbook.json()
    orderbook = orderbook['data']
    orderbook = orderbook[price_type]
    
    return orderbook

