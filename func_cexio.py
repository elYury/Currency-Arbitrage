#https://docs.plus.cex.io/#rest-public-api-calls-pairs-info

import requests

r = requests.get("https://api.plus.cex.io/rest-public/get_pairs_info")
r1 = requests.get("https://api.plus.cex.io/rest-public/get_ticker")


def get_cexio_symbols():
    info = r.json()
    info = info['data']
    sym_list = []

    for i in range(len(info)):
        if info[i]['quote'] == 'USDT':
            symbol = info[i]['base'] + '-' + info[i]['quote']
            sym_list.append(symbol)
        
    return sym_list

def get_cexio_ticker():
    ticker_list = []
    sym_list = get_cexio_symbols()
    ticker = r1.json()
    ticker = ticker['data']

    for i in range(len(sym_list)):
        for key in ticker:
            if sym_list[i] == key and float(ticker[key]["volume"]) >= 10000:
                symbol = sym_list[i].replace('-','')
                symbol_ticker = {symbol: ticker[key]['last']}
                ticker_list.append(symbol_ticker)

    # converts a list of dictionaries into a single dictionary
    sorteddict = {}
    for i in ticker_list:
        sorteddict.update(i)  

    return sorteddict

def get_cexio_orderbook(sym, outputask):
    if outputask == False:
        price_type = 'bids'
    else:
        price_type = 'asks'
    
    sym = sym.replace('USDT', '-USDT')
    orderbook = requests.get('https://api.plus.cex.io/rest-public/get_order_book?pair=' + sym)
    orderbook = orderbook.json()
    orderbook = orderbook['data']
    orderbook = orderbook[price_type]
    
    return orderbook

def get_cexio_d_w(sym, isWithdraw):
    return_info = []
    info = requests.get("https://api.plus.cex.io/rest-public/get_processing_info")
    info = info.json()
    info = info['data']

    for key in info:
        if key == sym:
            data = info[key]['blockchains']    
            for key in data:
                available = True
                network = data[key]["type"]
                if isWithdraw == True:
                    fee = data[key]["withdrawalFee"]
                    pcent_fee = data[key]["withdrawalFeePercent"]
                    if data[key]['withdrawal'] == 'disabled':
                        available = False 
                else:
                    fee = 0
                    pcent_fee = 0
                    if data[key]['deposit'] == 'disabled':
                        available = False
                if network == 'coin':
                    network = 'noData'
                dict = {'network': network, 'available': available, 'fee': fee, 'pcent_fee': pcent_fee}
                return_info.append(dict)

    return return_info


def get_cexio_link(symbol):
    sym = symbol.replace('USDT', '')
    link = 'https://cex.io/' + sym + '-usdt'
    return link

# ['algorand', 'avalanche', 'binancesmartchain', 'bitcoin', 'bitcoincash', 
#  'cardano', 'cosmos', 'cronos', 'dash', 'dogecoin', 'ethereum', 'ethereumpow', 
#  'everscale', 'fantom', 'flare', 'icp', 'kava', 'kusama', 'litecoin', 'metahash', 
#  'mina', 'neo', 'neo3', 'ontology', 'optimism', 'polkadot', 'polygon', 'ripple', 
#  'solana', 'songbird', 'stellar', 'terra', 'terra2', 'tezos', 'tron', 'xdc', 'zilliqa']