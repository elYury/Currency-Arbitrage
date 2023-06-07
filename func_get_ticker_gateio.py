import requests

host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
symbolurl = '/spot/currency_pairs'
tickerurl = '/spot/tickers'
query_param = ''

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
            if sym_list[i] == ticker[j]['currency_pair']:
                symbol = sym_list[i].replace("_", "")
                symbol_ticker = {symbol: ticker[j]['last']}
                ticker_list.append(symbol_ticker)
                
    sorteddict={}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict

#print(get_gateio_ticker())