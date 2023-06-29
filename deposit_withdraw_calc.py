# hitbtc has a function to find out the fee of transaction

import requests
from func_bybit import get_bybit_d_w

# NOTE: not all exchanges have a function to find out if 
# they are withdrawable or despoitable to default response is true

def deposit_withdraw(symbol, exchange_buy, exchange_sell):

    sym = symbol.replace('USDT', '')

# Buy exchanges (we only care if withdrawals are possible)
#______________________________________________________________

    if exchange_buy == 'Kucoin':
        info = requests.get("https://api.kucoin.com/api/v1/currencies/" + sym)
        info = info.json()
        info = info['data']
        if info['isWithdrawEnabled'] == False:
            return False
    
    if exchange_buy == 'Hitbtc': 
        info = requests.get("https://api.hitbtc.com/api/3/public/currency?currencies=" + sym)
        info = info.json()
        for key in info:
            if info[key]['payout_enabled'] == False:
                    return False
    
    if exchange_buy == 'Gate.io': 
        info = requests.get("https://api.gateio.ws/api/v4/spot/currencies/" + sym)
        info = info.json()
        if info['withdraw_disabled'] == True:
                return False
    
    if exchange_buy == 'Cex.io': 
        info = requests.get("https://api.plus.cex.io/rest-public/get_processing_info")
        info = info.json()
        info = info['data']
        for key in info:
            if info[key] == sym:
                data = info[key]['blockchains']     
                for key in data:
                    data[key]['withdrawal'] == 'disabled'
                    return False    
            return False
        
    if exchange_buy == 'Bitmart': 
        info = requests.get("https://api-cloud.bitmart.com/spot/v1/currencies")
        info = info.json()
        info = info['data']['currencies']
        for i in range(len(info)):
            if info[i]['id'] == sym and info[i]['withdraw_enabled'] == False:
                return False
            
    if exchange_buy == 'Bybit':
        if get_bybit_d_w(sym, True) == False:
            return False
            
# Sell exchanges (we only care if deposits are possible)
#______________________________________________________________

    if exchange_sell == 'Kucoin':
        info = requests.get("https://api.kucoin.com/api/v1/currencies/" + sym )
        info = info.json()
        info = info['data']
        if info['isDepositEnabled'] == False:
            return False
    
    if exchange_sell == 'Hitbtc': 
        info = requests.get("https://api.hitbtc.com/api/3/public/currency?currencies=" + sym)
        info = info.json()
        for key in info:
            if info[key]['payin_enabled'] == False:
                return False

    if exchange_sell == 'Gate.io': 
        info = requests.get("https://api.gateio.ws/api/v4/spot/currencies/" + sym)
        info = info.json()
        if info['deposit_disabled'] == True:
                return False
    
    if exchange_sell == 'Cex.io': 
        info = requests.get("https://api.plus.cex.io/rest-public/get_processing_info")
        info = info.json()
        info = info['data']
        for key in info:
            if info[key] == sym:
                data = info[key]['blockchains']    
                for key in data:
                    data[key]['deposit'] == 'disabled'
                    return False
    
    if exchange_sell == 'Bitmart': 
        info = requests.get("https://api-cloud.bitmart.com/spot/v1/currencies")
        info = info.json()
        info = info['data']['currencies']
        for i in range(len(info)):
            if info[i]['id'] == sym and info[i]['deposit_enabled'] == False:
                return False
            
    if exchange_sell == 'Bybit':
        if get_bybit_d_w(sym, False) == False:
            return False

    return True


#TODO: Binance https://api.binance.com/sapi/v1/capital/config/getall



#print(deposit_withdraw('SAITAMA','Bybit', 'x'))


#NOTE: NO easy way of getting withdrawal/deposit status for the following exchanges
            # OKX
            # KRAKEN
            # HOTCOIN GLOBAL
            # 

#gate.io has fixed rate param, and chain

#bybit has % fee and currency fee and chain