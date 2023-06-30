
# CONFIGURATION OF ARBITRAGE BOT FILE
#_________________________________________________________________-

# Used to stop text to speech (False = no text to speech)
txt_to_speech = False

# Minimum difference between market prices when fetching ticker in order to identifiy potential arbitrage opportunities
# Measured in %
minimum_difference = 2.5

# Estimation of fees, the bot will not take arbitrage opportunities which yield a smaller return than the estimation of fees
# Measured in USDT
minimum_usdt_amount = 15

# Buffer changes the buy cap (-) and sell cap (+) by the given %
# Measured in decimal 0.1 = 10%, 0.9 = 90%, tu eres listo eh
buffer = 0.1

# Does exactly what you think
# Measured in seconds
pause_between_runs = 60

# list of exchanges where withdraw and deposit data is lacking
no_data_list = ['Hotcoin_Global', 'OKX', 'Kraken']

# Ban list of cases where cryptos are not the same on different exchanges but share the same name format [{symbol: XXX, exchange_buy: Xxxx, exchange_sell: Xxxx},{},...]

ban_list =[{'symbol': 'AIUSDT', 'exchange_buy': 'Hotcoin_Global', 'exchange_sell': 'Kucoin'}, 
           {'symbol': 'ANCUSDT', 'exchange_buy': 'Kucoin', 'exchange_sell': 'Gate.io'}, 
           {'symbol': 'ANCUSDT', 'exchange_buy': 'Kucoin', 'exchange_sell': 'Bitmart'}, 
           {'symbol': 'BFCUSDT', 'exchange_buy': 'Hotcoin_Global', 'exchange_sell': 'Kucoin'}, 
           {'symbol': 'BFCUSDT', 'exchange_buy': 'Hotcoin_Global', 'exchange_sell': 'Gate.io'}, 
           {'symbol': 'BFTUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'Hotcoin_Global'}, 
           {'symbol': 'BTGUSDT', 'exchange_buy': 'Hotcoin_Global', 'exchange_sell': 'Gate.io'}, 
           {'symbol': 'BUYUSDT', 'exchange_buy': 'Kucoin', 'exchange_sell': 'Gate.io'}, 
           {'symbol': 'DYPUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'Kucoin'}, 
           {'symbol': 'FAMEUSDT', 'exchange_buy': 'Bybit', 'exchange_sell': 'Gate.io'},
           {'symbol': 'FAMEUSDT', 'exchange_buy': 'OKX', 'exchange_sell': 'Bybit'}, 
           {'symbol': 'HECUSDT', 'exchange_buy': 'Hotcoin_Global', 'exchange_sell': 'Bitmart'}, 
           {'symbol': 'MMMUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'Kucoin'}, 
           {'symbol': 'PLCUUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'Bitmart'}, 
           {'symbol': 'PRMXUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'Kucoin'}, 
           {'symbol': 'SWPUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'Kucoin'}, 
           {'symbol': 'TEMUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'Kucoin'}, 
           {'symbol': 'WSBUSDT', 'exchange_buy': 'Gate.io', 'exchange_sell': 'OKX'},
           {'symbol': 'WSBUSDT', 'exchange_buy': 'Bitmart', 'exchange_sell': 'Bybit'}]

# SECTION FOR API KEYS, SECRETS, AND PASSCODES
#_________________________________________________________________-


