#https://docs.kucoin.com/#hftrading

import requests
from kucoin.client import Market

client = Market(key='no key for you', secret='no pass for you', passphrase=';)', url='https://openapi-v2.kucoin.com')


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

def get_kucoin_d_w(sym, isWithdraw):
    info = requests.get("https://api.kucoin.com/api/v2/currencies/" + sym)
    info = info.json()
    info = info['data']['chains']
    return_info = []

    for i in range(len(info)):
        available = True
        network = info[i]['chainName']
        if isWithdraw == True:
            fee = info[i]['withdrawalMinFee']
            if info[i]['isWithdrawEnabled'] == False:
                available = False
        else:
            fee = 0
            if info[i]['isDepositEnabled'] == False:
                available = False
            
        dict = {'network': network, 'available': available, 'fee': fee, 'pcent_fee': 'noData'}
        return_info.append(dict)
    
    return return_info


def get_kucoin_link(symbol):
    sym = symbol.replace('USDT', '')
    link = 'https://www.kucoin.com/trade/' + sym + '-USDT'
    return link
  
