#https://bybit-exchange.github.io/docs/linear/#t-introduction

from pybit.unified_trading import HTTP
from pybit.unified_trading import WebSocket

#APIkey = "rVMWSWoabYl8OVisI0"
#APIsecret = "rAmkTaGjUYiHY9bPSlkLjSzoKq2iIUXpsUl8"

#api_url = "https://api-testnet.bybit.com"

session = HTTP(
    testnet=True,
    api_key="rVMWSWoabYl8OVisI0",
    api_secret="rAmkTaGjUYiHY9bPSlkLjSzoKq2iIUXpsUl8",
)
def get_tradeable_symbols():

    # Get available symbols
    sym_list = []
    symbols = session.query_symbol()
    if "ret_msg" in symbols.keys():
        if symbols["ret_msg"] == "OK":
            symbols = symbols["result"]
            for symbol in symbols:
                if symbol["quote_currency"] == "USDT" and symbol["status"] == "Trading":
                    sym_list.append(symbol)
    # Return ouput
    return sym_list

symbol_list = get_tradeable_symbols()

for i in range(len(symbol_list)):
    btc_ticker = session.get_tickers(
        category = "inverse",
        symbol = symbol_list[i],
    )
    print(btc_ticker['result']['list'][0]['lastPrice'])


