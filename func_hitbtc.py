#https://api.hitbtc.com/
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
            if sym_list[i] == key and float(ticker[key]["volume_quote"]) >= 10000:
                symbol = sym_list[i]
                symbol_ticker = {symbol: ticker[key]['last']}
                ticker_list.append(symbol_ticker)
    
    # converts a list of dictionaries into a single dictionary
    sorteddict = {}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict


# List inside a List [[price, amount], [price, amount]...]
def get_hitbtc_orderbook(sym, outputask):
    if outputask == False:
        price_type = 'bid'
    else:
        price_type = 'ask'
    
    orderbook = requests.get('https://api.hitbtc.com/api/3/public/orderbook?depth=100')
    orderbook = orderbook.json()
    orderbook = orderbook[sym][price_type]
    
    return orderbook

def get_hitbtc_d_w(sym, isWithdraw):
    info = requests.get("https://api.hitbtc.com/api/3/public/currency?currencies=" + sym)
    info = info.json()
    return_info = []
    for key in info:
        available = True
        info = info[key]['networks']
        for i in range(len(info)):
            network = info[i]['network']
            if isWithdraw == True:
                fee = info[i]['payout_fee']
                if info[i]['payout_enabled'] == False:
                    available = False
            else:
                fee = 0
                if info[key]['payin_enabled'] == False:
                    available = False

            dict = {'network': network, 'available': available, 'fee': fee, 'pcent_fee': 'noData'}
            return_info.append(dict)

    return return_info

def get_hitbtc_link(symbol):
    sym = symbol.replace('USDT', '')
    link = 'https://hitbtc.com/' + sym + '-to-usdt'
    return link
