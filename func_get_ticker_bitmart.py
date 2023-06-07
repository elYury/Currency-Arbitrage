#reference
#https://developer-pro.bitmart.com/en/spot/#get-list-of-trading-pair-details

import requests

r = requests.get('https://api-cloud.bitmart.com/spot/v1/symbols/details')
r1 = requests.get('https://api-cloud.bitmart.com/spot/v2/ticker')

def get_bitmart_symbols():

    info = r.json()
    info = info['data']['symbols']
    sym_list = []

    for x in range(len(info)):
        if info[x]['quote_currency'] == 'USDT' and info[x]['trade_status'] == 'trading':
            sym_list.append(info[x]['symbol'])

    return sym_list


def get_bitmart_ticker():
    ticker_list = []
    sym_list = get_bitmart_symbols()
    ticker = r1.json()
    ticker = ticker["data"]["tickers"]

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['symbol']:
                symbol = sym_list[i].replace("_", "")
                symbol_ticker = {symbol: ticker[j]['last_price']}
                ticker_list.append(symbol_ticker)
                
    sorteddict={}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict

#print(get_bitmart_ticker())