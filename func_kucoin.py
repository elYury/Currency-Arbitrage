#https://docs.kucoin.com/#hftrading

import requests
from kucoin.client import Market

client = Market(key='647f1dd6a19a0000016203f6', secret='5ab47452-b349-413a-85f4-0642421864c5', passphrase='kucoinhasagoodapim8', url='https://openapi-v2.kucoin.com')


def get_kucoin_symbols():

    info = client.get_symbol_list()

    sym_list = []

    for x in range(len(info)):
        if info[x]['quoteCurrency'] == 'USDT' and info[x]['enableTrading'] == True:
            sym_list.append(info[x]['name'])

    return sym_list


def get_kucoin_ticker():

    ticker_list = []
    sym_list = get_kucoin_symbols()
    ticker = client.get_all_tickers()

    ticker = ticker["ticker"]

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['symbol'] and float(ticker[j]["volValue"]) >= 10000:
                symbol = sym_list[i].replace("-", "")
                symbol_ticker = {symbol: ticker[j]['last']}
                ticker_list.append(symbol_ticker)
                
    sorteddict={}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict


def get_kucoin_orderbook(sym, outputask):
    if outputask == False:
        price = 'bids'
    else:
        price = 'asks'
    sym = sym.replace("USDT", "-USDT")
    orderbook = requests.get('https://api.kucoin.com/api/v1/market/orderbook/level2_100?symbol=' + sym)
    orderbook = orderbook.json()
    orderbook = orderbook['data'][price]
    
    return orderbook


#print(get_kucoin_orderbook('BTCUSDT', False))