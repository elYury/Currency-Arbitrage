#API Bybit
#APIkey = "rVMWSWoabYl8OVisI0"
#APIsecret = "rAmkTaGjUYiHY9bPSlkLjSzoKq2iIUXpsUl8"

#CdW6mWuIVLIsR5KCwu
#VGGnB4ZjEg7N3GyDUTiK1JHogH7bI41UpHEA

from pybit.unified_trading import HTTP

def get_sym_list():
    session = HTTP(testnet=False)
    info = session.get_instruments_info(
        category="spot"
    )
    sym_list = []

    info = info['result']['list']
    for x in range(len(info)):
        if info[x]['quoteCoin'] == 'USDT' and info[x]['status'] == 'Trading':
            sym_list.append(info[x]['symbol'])

    return sym_list


def get_bybit_ticker():
    session = HTTP(testnet=False)
    info = session.get_instruments_info(
    category="spot")
    sym_list = get_sym_list()
    ticker_list = []
    ticker = session.get_tickers(category="spot")
    ticker = ticker['result']['list']

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['symbol']:
                symbol_ticker = {sym_list[i]: ticker[j]['lastPrice']}
                ticker_list.append(symbol_ticker)
    
    return ticker_list
    
#print(get_bybit_ticker())
