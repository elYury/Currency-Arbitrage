from kucoin.client import Market


def get_kucoin_ticker():
    client = Market(key='647f1dd6a19a0000016203f6', secret='5ab47452-b349-413a-85f4-0642421864c5', passphrase='kucoinhasagoodapim8', url='https://openapi-v2.kucoin.com')

    info = client.get_symbol_list()

    sym_list = []

    for x in range(len(info)):
        if info[x]['quoteCurrency'] == 'USDT' and info[x]['enableTrading'] == True:
            sym_list.append(info[x]['symbol'])

    ticker_list = []

    ticker = client.get_all_tickers()

    ticker = ticker["ticker"]

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['symbol']:
                symbol = sym_list[i].replace("-", "")
                symbol_ticker = {symbol: ticker[j]['last']}
                ticker_list.append(symbol_ticker)
        
    return ticker_list
#print(get_kucoin_ticker())