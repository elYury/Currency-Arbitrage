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
            if sym_list[i] == ticker[j]['symbol'] and float(ticker[j]['quote_volume_24h']) >= 10000:
                symbol = sym_list[i].replace("_", "")
                symbol_ticker = {symbol: ticker[j]['last_price']}
                ticker_list.append(symbol_ticker)
                
    sorteddict={}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict

#https://api-cloud.bitmart.com/spot/v1/symbols/book?symbol=BTC_USDT

def get_bitmart_orderbook(sym, outputask):
    if outputask == False:
        ask_bid = 'buys'
    else:
        ask_bid = 'sells'
    sym = sym.replace("USDT", "_USDT")
    orderbook = requests.get('https://api-cloud.bitmart.com/spot/v1/symbols/book?symbol=' + sym + '&size=100')
    orderbook = orderbook.json()
    orderbook = orderbook['data'][ask_bid]

    # We need to convert the list of dictionaries into a list of lists 
    # make a new list
    res = []
    # Iterate over i, sub is the sub division of the dictionary ex. [{sub i=0},{sub i=1}...]
    for i, sub in enumerate(orderbook, start = 0):
        #delete the keys that we do not need (we only need price and amount)
        del orderbook[i]['total']
        del orderbook[i]['count']
        #append the values that are left to the new list(index = i ) of lists
        res.append(list(sub.values()))
        #we need price to appear first, followed by amount therefore we do a quick tmp switch-a-roo
        tmp = res[i][0]
        res[i][0] = res[i][1]
        res[i][1] = tmp

    return res

def get_bitmart_d_w(sym, isWithdraw):
    info = requests.get("https://api-cloud.bitmart.com/account/v1/currencies")
    info = info.json()
    info = info['data']['currencies']
    return_info = []
    
    for i in range(len(info)):
        if info[i]['currency'] == sym:
            available = True
            network = info[i]['network']
            if isWithdraw == True:
                fee = info[i]['withdraw_minfee']
                if info[i]['deposit_enabled'] == False:
                    available = False
            else:
                fee = 0
                if info[i]['withdraw_enabled'] == False:
                    available = False

            dict = {'network': network, 'available': available, 'fee': fee, 'pcent_fee': 'noData'}
            return_info.append(dict)

    return return_info

def get_bitmart_link(symbol):
    sym = symbol.replace('USDT', '')
    link = 'https://www.bitmart.com/trade/en-US?layout=pro&theme=dark&symbol=' + sym + '_USDT'
    return link