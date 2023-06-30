# hitbtc has a function to find out the fee of transaction

import requests
from func_bybit import get_bybit_d_w, get_bybit_link
from func_binance import get_binance_d_w, get_binance_link
from func_bitmart import get_bitmart_d_w, get_bitmart_link
from func_cexio import get_cexio_d_w, get_cexio_link
from func_gateio import get_gateio_d_w, get_gateio_link
from func_hitbtc import get_hitbtc_d_w, get_hitbtc_link
from func_kucoin import get_kucoin_d_w, get_kucoin_link
from func_okx import get_okx_link
from func_kraken import get_kraken_link
from func_hotcoinglobal import get_hotcoinglobal_link

from config import no_data_list

# NOTE: not all exchanges have a function to find out if 
# they are withdrawable or despoitable to default response is true

def get_withdrawal(symbol, exchange):

    sym = symbol.replace('USDT', '')

    # Buy exchanges (we only care if withdrawals are possible)
    if exchange == 'Kucoin':
        withdrawal_data = get_kucoin_d_w(sym, True)
    if exchange == 'Hitbtc': 
        withdrawal_data = get_hitbtc_d_w(sym, True)
    if exchange == 'Gate.io': 
        withdrawal_data = get_gateio_d_w(sym, True)
    if exchange == 'Cex.io': 
        withdrawal_data = get_cexio_d_w(sym, True)
    if exchange == 'Bitmart': 
        withdrawal_data = get_bitmart_d_w(sym, True)
    if exchange == 'Bybit':
        withdrawal_data = get_bybit_d_w(sym, True)
    if exchange == 'Binance':
        withdrawal_data = get_binance_d_w(sym, True)

    if exchange in no_data_list:
        withdrawal_data = [{'network': 'noData', 'available': True, 'fee': 'noData', 'pcent_fee': 'noData'}]

    return withdrawal_data


def get_deposit(symbol, exchange):

    sym = symbol.replace('USDT', '')

    # Sell exchanges (we only care if deposits are possible)
    if exchange == 'Kucoin':
        deposit_data = get_kucoin_d_w(sym, False)
    if exchange == 'Hitbtc': 
        deposit_data = get_hitbtc_d_w(sym, False)
    if exchange == 'Gate.io': 
        deposit_data = get_gateio_d_w(sym, False)
    if exchange == 'Cex.io': 
        deposit_data = get_cexio_d_w(sym, False)
    if exchange == 'Bitmart': 
        deposit_data = get_bitmart_d_w(sym, False)
    if exchange == 'Bybit':
        deposit_data = get_bybit_d_w(sym, False)
    if exchange == 'Binance':
        deposit_data = get_binance_d_w(sym, False) 
    
    if exchange in no_data_list:
        deposit_data = [{'network': 'noData', 'available': True, 'fee': 'noData', 'pcent_fee': 'noData'}]
        
    return deposit_data

def get_link(exchange, sym):

    if exchange == 'Kucoin':
        link = get_kucoin_link(sym)
    if exchange == 'Hitbtc': 
        link = get_hitbtc_link(sym)
    if exchange == 'Gate.io': 
        link = get_gateio_link(sym)
    if exchange == 'Cex.io': 
        link = get_cexio_link(sym)
    if exchange == 'Bitmart': 
        link = get_bitmart_link(sym)
    if exchange == 'Bybit':
        link = get_bybit_link(sym)
    if exchange == 'Binance':
        link = get_binance_link(sym)
    if exchange == 'Hotcoin_Global':
        link = get_hotcoinglobal_link(sym)
    if exchange == 'OKX':
        link = get_okx_link(sym)
    if exchange == 'Kraken':
        link = get_kraken_link(sym)
    return link


#NOTE: NO easy way of getting withdrawal/deposit status for the following exchanges
            # OKX
            # KRAKEN
            # HOTCOIN GLOBAL


# BINANCE
#https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data
#Binance has chain, fee and esimated arrival time
# fee
# https://binance-docs.github.io/apidocs/spot/en/#asset-detail-user_data

# BYbit
#https://bybit-exchange.github.io/docs/v5/asset/coin-info
#bybit has % fee and currency fee and chain
# fee
# https://bybit-exchange.github.io/docs/v5/account/fee-rate

# BITMART
#https://developer-pro.bitmart.com/en/spot/#get-currencies
#bitmart has chains and withdrawal min fee
# i need to change the api call to the above link
# fee 
# https://developer-pro.bitmart.com/en/spot/#get-actual-trade-fee-rate-keyed

# CEX.IO
#https://docs.plus.cex.io/#rest-public-api-calls-processing-info
#cex.io has chains but they are in a stupid format + has withdrawal fees
#trading fee
#https://docs.plus.cex.io/#rest-private-api-calls-fee

# GATE.IO
#https://www.gate.io/docs/developers/apiv4/en/#retrieve-withdrawal-status
# and 
#https://www.gate.io/docs/developers/apiv4/en/#list-chains-supported-for-specified-currency
# Fixed withdrawal fee on chains + fixed withdrawal fee ? or not
#gate.io has fixed rate param, and chain
# fee
#https://www.gate.io/docs/developers/apiv4/en/#retrieve-personal-trading-fee

# HITBTC
# https://api.hitbtc.com/#currencies
# has withdrawal fee, and chains
# fee
# https://api.hitbtc.com/#get-all-trading-commissions

# HOTCOINGLOBAL

# KRAKEN

# KUCOIN
# https://docs.kucoin.com/#get-currency-detail-recommend
# chains, and withdrawal fees
# fee 
# https://docs.kucoin.com/#actual-fee-rate-of-the-trading-pair


# OKX
