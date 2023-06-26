#https://www.okx.com/docs-v5/en/?shell#rest-api-public-data-get-instruments

import requests

host = "https://www.okx.com"
prefix = "/api/v5"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
symbolurl = '/public/instruments?instType=SPOT'
tickerurl = '/market/tickers?instType=SPOT'
orderbookurl = '/market/books?instId='

r = requests.request('GET', host + prefix + symbolurl, headers=headers)
r1 = requests.request('GET', host + prefix + tickerurl, headers=headers)

def get_okx_symbols():

    info = r.json()
    info = info['data']
    sym_list = []

    for x in range(len(info)):
        if info[x]['quoteCcy'] == 'USDT' and info[x]['state'] == 'live': 
            sym_list.append(info[x]['instId'])

    return sym_list


def get_okx_ticker():
    ticker_list = []
    sym_list = get_okx_symbols()
    ticker = r1.json()
    ticker = ticker['data']

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['instId'] and float(ticker[j]['vol24h']) >= 10000: 
                symbol = sym_list[i].replace("-", "")
                symbol_ticker = {symbol: ticker[j]['last']}
                ticker_list.append(symbol_ticker)
                
    sorteddict={}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict

def get_okx_orderbook(sym, outputask):
    if outputask == False:
        price = 'bids'
    else:
        price = 'asks'

    sym = sym.replace("USDT", "-USDT")
    orderbook = requests.get('https://www.okx.com/api/v5/market/books?instId=' + sym + '&sz=100')
    orderbook = orderbook.json()
    orderbook = orderbook['data'][0][price]

    for i in range(len(orderbook)):
        # delete the 3rd and 4th item in the list (we only need price and volume)
        del orderbook[i][2]
        del orderbook[i][2]

    return orderbook

