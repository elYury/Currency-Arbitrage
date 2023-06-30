#https://docs.kraken.com/rest/#tag/Market-Data/operation/getTickerInformation
import requests

r = requests.get("https://api.kraken.com/0/public/AssetPairs")
r1 = requests.get("https://api.kraken.com/0/public/Ticker")


def get_kraken_symbols():
    info = r.json()
    info = info['result']
    sym_list = []

    for key in info:
        if info[key]['quote'] == 'USDT' and info[key]['status'] == 'online':
            sym_list.append(key)
        
    return sym_list

def get_kraken_ticker():
    ticker_list = []
    sym_list = get_kraken_symbols()
    ticker = r1.json()
    ticker = ticker['result']

    for i in range(len(sym_list)):
        for key in ticker:
            if sym_list[i] == key and float(ticker[key]["v"][1]) >= 10000 :
                symbol = sym_list[i]
                symbol_ticker = {symbol: ticker[key]['c'][0]}
                ticker_list.append(symbol_ticker)
                
    sorteddict = {}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict



def get_kraken_orderbook(sym, outputask):
    if outputask == False:
        price_type = 'bids'
    else:
        price_type = 'asks'
    
    orderbook = requests.get('https://api.kraken.com/0/public/Depth?pair=' + sym)
    orderbook = orderbook.json()
    orderbook = orderbook['result']
    orderbook = orderbook[sym][price_type]

    
    for i in range(len(orderbook)):
        del orderbook[i][2]
    
    return orderbook


def get_kraken_link(symbol):
    sym = symbol.replace('USDT', '')
    link = 'https://pro.kraken.com/app/trade/' + sym + '_usdt'
    return link
