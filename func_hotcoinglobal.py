#https://hotcoinex.github.io/en/spot/market.html#real-time-ticker-data
import requests

r = requests.get("https://api.hotcoinfin.com/v1/common/symbols")
r1 = requests.get("https://api.hotcoinfin.com/v1/market/ticker")


def get_hotcoinglobal_symbols():
    info = r.json()
    info = info['data']
    sym_list = []

    for i in range(len(info)):
        if info[i]['symbol'].endswith('_usdt') and info[i]['state'] == 'enable': #quote currency does not work on the api
            sym_list.append(info[i]['symbol'])
        
    return sym_list


def get_hotcoinglobal_ticker():
    ticker_list = []
    sym_list = get_hotcoinglobal_symbols()
    ticker = r1.json()
    ticker = ticker['ticker']

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['symbol'] and float(ticker[j]["vol"]) >= 10000:
                symbol = sym_list[i].replace("_", "").upper()
                symbol_ticker = {symbol: ticker[j]['last']}
                ticker_list.append(symbol_ticker)
                
    sorteddict = {}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict


def get_hotcoinglobal_orderbook(sym, outputask):
    if outputask == False:
        price_type = 'bids'
    else:
        price_type = 'asks'
    
    sym = sym.replace('USDT', "_USDT").lower()
    orderbook = requests.get('https://api.hotcoinfin.com/v1/depth?symbol=' + sym + '&step=100')
    orderbook = orderbook.json()
    orderbook = orderbook['data']['depth']
    orderbook = orderbook[price_type]
    
    return orderbook


def get_hotcoinglobal_link(symbol):
    sym = symbol.replace('USDT', '')
    link = 'https://hotcoin.com/currencyExchangeTwo/' + sym + '_usdt'
    return link

