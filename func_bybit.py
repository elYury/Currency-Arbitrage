#API Bybit https://bybit-exchange.github.io/docs/v5/intro

#CdW6mWuIVLIsR5KCwu
#VGGnB4ZjEg7N3GyDUTiK1JHogH7bI41UpHEA

from pybit.unified_trading import HTTP

session = HTTP(testnet=False,
                api_key="CdW6mWuIVLIsR5KCwu",
                api_secret="VGGnB4ZjEg7N3GyDUTiK1JHogH7bI41UpHEA",)

def get_bybit_symbols():
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
    sym_list = get_bybit_symbols()
    ticker_list = []
    ticker = session.get_tickers(category="spot")
    ticker = ticker['result']['list']

    for i in range(len(sym_list)):
        for j in range(len(ticker)):
            if sym_list[i] == ticker[j]['symbol'] and float(ticker[j]['turnover24h']) >= 10000:
                symbol_ticker = {sym_list[i]: ticker[j]['lastPrice']}
                ticker_list.append(symbol_ticker)
    
    sorteddict={}
    for i in ticker_list:
        sorteddict.update(i) 

    return sorteddict

def get_bybit_orderbook(sym, outputask):
    if outputask == False:
        price = 'b'
    else:
        price = 'a'

    orderbook = session.get_orderbook(
        category="spot",
        symbol=sym,
        limit = 100
        )
    orderbook = orderbook['result'][price]
    return orderbook

# We have the ability to look at % fee and currency fee
# We also have the ability to look at the chaintype
def get_bybit_d_w(sym, isWithdraw):
    return_info = []
    info = session.get_coin_info(coin=sym)
    info = info['result']['rows']
    
    for i in range(len(info)):
        network_data = info[i]['chains']

        for j in range(len(network_data)):
            pcent_fee = 0
            network = network_data[j]['chain']
            available = True
            if isWithdraw == True:
                fee = network_data[j]['withdrawFee']
                pcent_fee = network_data[j]["withdrawPercentageFee"]
                if network_data[j]['withdrawFee'] == '' or network_data[j]['chainWithdraw'] == 0:
                    available = False
            else:
                fee = 0
                if network_data[j]['chainDeposit'] == 0:
                    available = False

            dict = {'network': network, 'available': available, 'fee': fee, 'pcent_fee': pcent_fee}
            return_info.append(dict)

    return return_info


def get_bybit_link(symbol):
    sym = symbol.replace('USDT', '')
    link = 'https://www.bybit.com/en-US/trade/spot/' + sym + '/USDT'
    return link