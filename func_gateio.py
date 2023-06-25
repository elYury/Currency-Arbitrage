#https://www.gate.io/docs/developers/apiv4/en/

import requests

host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
symbolurl = '/spot/currency_pairs'
tickerurl = '/spot/tickers'

r = requests.request('GET', host + prefix + symbolurl, headers=headers)
r1 = requests.request('GET', host + prefix + tickerurl, headers=headers)


def get_gateio_symbols():

    info = r.json()

    sym_list = []

    for x in range(len(info)):
        if info[x]['quote'] == 'USDT' and info[x]['trade_status'] == 'tradable': 
            sym_list.append(info[x]['id'])

    return sym_list


def get_gateio_ticker():
    ticker_list = []
    sym_list = get_gateio_symbols()
    ticker = r1.json()

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['currency_pair']: #there is no volume on this request #and float(info[x]['quote_volume']) >= 10000:
                symbol = sym_list[i].replace("_", "")
                symbol_ticker = {symbol: ticker[j]['last']}
                ticker_list.append(symbol_ticker)
                
    sorteddict={}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict

def get_gateio_orderbook(sym, outputask):
    if outputask == False:
        price = 'bids'
    else:
        price = 'asks'

    sym = sym.replace("USDT", "_USDT")
    orderbook = requests.get('https://api.gateio.ws/api/v4/spot/order_book?currency_pair=' + sym + '&limit=100')
    orderbook = orderbook.json()
    orderbook = orderbook[price]
    
    return orderbook

#print(get_gateio_orderbook('BTCUSDT', False))