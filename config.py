
# CONFIGURATION OF ARBITRAGE BOT FILE
#_________________________________________________________________-

# Used to stop text to speech (False = no text to speech)
txt_to_speech = False

# Balance available to trade with in USDT
balance = 1000

# Minimum difference between market prices when fetching ticker in order to identifiy potential arbitrage opportunities
# Measured in %
minimum_difference = 2.5

# Estimation of fees, the bot will not take arbitrage opportunities which yield a smaller return than the estimation of fees
# Measured in USDT
minimum_usdt_amount = 20

# Buffer changes the buy cap (-) and sell cap (+) by the given %
# Measured in decimal 0.1 = 10%, 0.9 = 90%, tu eres listo eh
buffer = 0.1

# Does exactly what you think
# Measured in seconds
pause_between_runs = 60

# list of exchanges where withdraw and deposit data is lacking
no_data_list = ['Hotcoin_Global', 'OKX', 'Kraken']

# Takers fee list
takers = {'Binance': 0.1, 'Hotcoin_Global': 0.2, 
          'Pionex': 0.05, 'Bitforex': 0.1, 
          'OKX': 0.1, 'Upbit': 0.2, 
          'Coinbase_Pro': 0.6, 'Coinw': 0.2, 
          'Bybit': 0.1, 'Kraken': 0.26, 
          'Tapbit': 0.1, 'Kucoin': 0.1, 
          'Bitget': 0.1, 'Bitmart': 0.1, 
          'Hitbtc': 0.25, 'Gate.io': 0.2, 
          'Btcex': 0.1, 'Lbank': 0.1, 
          'Mexc': 0, 'XT.com': 0.2, 
          'P2B': 0.2, 'Bkex': 0.2, 
          'Toobit': 0.2, 'Huobi': 0.2, 
          'Cointr_Pro': 0.2, 'Bitstramp': 0.4, 
          'Bitfinex': 0.2, 'Latoken': 0.5, 
          'Crypto.com': 0.075, 'Bitflyer': 0.15, 
          'Poloniex': 0.2, 'Gemini': 0.4, 
          'Bitmex': 0.075, 'Cex.io': 0.25}

# Ban list of cases where cryptos are not the same on different exchanges but share the same name format [{symbol: XXX, exchange_buy: Xxxx, exchange_sell: Xxxx},{},...]
ban_list = [{'symbol': 'BOXUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'Hotcoin_Global'}]

# SECTION FOR API KEYS, SECRETS, AND PASSCODES
#_________________________________________________________________-


