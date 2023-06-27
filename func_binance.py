# from binance.client import Client

# api_key = "gKHnjT4bo0aZlqwVMp1XK25kXoVCQkoo8Iu9bNrqrwgwAbpP2m2WPJ0ruSvtJb1q"
# api_secret = "0R5Y9IMzovnsb9cAmdH1EqsNFb5xLKqORPtV4lvAqFJW6iY53bd6soQ0KJtrf3S3"

# client = Client(api_key, api_secret)
# print("loggged in")

#https://binance-docs.github.io/apidocs/spot/en/#check-server-time
import requests

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

#print(get_binance_orderbook('ORNUSDT', False))