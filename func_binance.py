#https://binance-docs.github.io/apidocs/spot/en/#check-server-time

import requests
from binance.client import Client

api_key = "gKHnjT4bo0aZlqwVMp1XK25kXoVCQkoo8Iu9bNrqrwgwAbpP2m2WPJ0ruSvtJb1q"
api_secret = "0R5Y9IMzovnsb9cAmdH1EqsNFb5xLKqORPtV4lvAqFJW6iY53bd6soQ0KJtrf3S3"

client = Client(api_key, api_secret)

r = requests.get("https://api.binance.com/api/v3/exchangeInfo")
r1 = requests.get("https://api.binance.com/api/v3/ticker/price")


def get_binance_symbols():
    info = r.json()
    info = info['symbols']
    sym_list = []

    for i in range(len(info)):
        if info[i]['quoteAsset'] == 'USDT' and info[i]['status'] == 'TRADING' and info[i]["isSpotTradingAllowed"] == True:
            sym_list.append(info[i]['symbol'])
        
    return sym_list

def get_binance_ticker():
    ticker_list = []
    sym_list = get_binance_symbols()
    ticker = r1.json()

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['symbol']: #Volume not available
                symbol = sym_list[i]
                symbol_ticker = {symbol: ticker[j]['price']}
                ticker_list.append(symbol_ticker)
    
    # converts a list of dictionaries into a single dictionary
    sorteddict = {}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict


def get_binance_orderbook(sym, outputask):
    if outputask == False:
        price_type = 'bids'
    else:
        price_type = 'asks'
    
    orderbook = requests.get('https://api.binance.com/api/v3/depth?symbol=' + sym)
    orderbook = orderbook.json()
    orderbook = orderbook[price_type]
    
    return orderbook
#Doc
#https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data
# HTTP API
#https://api.binance.com/sapi/v1/capital/config/getall

def get_binance_d_w(sym, isWithdraw):
    return_info = []
    info = client.get_all_coins_info()
    for i in range(len(info)):
        if info[i]['coin'] == sym:
            network_data = info[i]['networkList']

            # Return True if at least one network is available
            for j in range(len(network_data)):
                network = network_data[j]['network']
                available = True
                if isWithdraw == True:
                    fee = network_data[j]['withdrawFee']
                    if network_data[j]['withdrawEnable'] == False:
                        available = False
                else:
                    fee = 0
                    if network_data[j]['depositEnable'] == False:
                        available = False

                dict = {'network': network, 'available': available, 'fee': fee, 'pcent_fee': 'noData'}
                return_info.append(dict)

    return return_info 

