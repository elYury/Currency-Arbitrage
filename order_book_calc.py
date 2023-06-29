
from config import buffer

from func_bybit import get_bybit_orderbook
from func_bitmart import get_bitmart_orderbook
from func_gateio import get_gateio_orderbook
from func_hitbtc import get_hitbtc_orderbook
from func_kucoin import get_kucoin_orderbook
from func_kraken import get_kraken_orderbook
from func_okx import get_okx_orderbook
from func_hotcoinglobal import get_hotcoinglobal_orderbook
from func_cexio import get_cexio_orderbook
from func_binance import get_binance_orderbook

# ex. bybit = get_""""""_orderbook(symbol, here we put the type of price we are looking for, true = ask)

#-------------------------------------------------------------------------------------------------------------------

def orderbook_info(symbol, exchange_buy, exchange_sell):

    # ASKS
    #request asks from orderbook at the exchange we are trying to buy crypto

    if exchange_buy == 'Bybit':
        orderbook_asks = get_bybit_orderbook(symbol, True)
    elif exchange_buy == 'Bitmart':
        orderbook_asks = get_bitmart_orderbook(symbol, True)
    elif exchange_buy == 'Gate.io':
        orderbook_asks = get_gateio_orderbook(symbol, True)
    elif exchange_buy == 'Hitbtc':
        orderbook_asks = get_hitbtc_orderbook(symbol, True)
    elif exchange_buy == 'Kucoin':
        orderbook_asks = get_kucoin_orderbook(symbol, True)
    elif exchange_buy == 'Kraken':
        orderbook_asks = get_kraken_orderbook(symbol, True)
    elif exchange_buy == 'OKX':
        orderbook_asks = get_okx_orderbook(symbol, True)
    elif exchange_buy == 'Hotcoin_Global':
        orderbook_asks = get_hotcoinglobal_orderbook(symbol, True)
    elif exchange_buy == 'Cex.io':
        orderbook_asks = get_cexio_orderbook(symbol, True)
    elif exchange_buy == 'Binance':
        orderbook_asks = get_binance_orderbook(symbol, True)

        
    #-------------------------------------------------------------------------------------------------------------------
    # BIDS
    #request bids from orderbook at the exchange we are trying to sell crypto
   
    if exchange_sell == 'Bybit':
        orderbook_bids = get_bybit_orderbook(symbol, False)
    elif exchange_sell == 'Bitmart':
        orderbook_bids = get_bitmart_orderbook(symbol, False)
    elif exchange_sell == 'Gate.io':
        orderbook_bids = get_gateio_orderbook(symbol, False)
    elif exchange_sell == 'Hitbtc':
        orderbook_bids = get_hitbtc_orderbook(symbol, False)
    elif exchange_sell == 'Kucoin':
        orderbook_bids = get_kucoin_orderbook(symbol, False)
    elif exchange_sell == 'Kraken':
        orderbook_bids = get_kraken_orderbook(symbol, False)
    elif exchange_sell == 'OKX':
        orderbook_bids = get_okx_orderbook(symbol, False)
    elif exchange_sell == 'Hotcoin_Global':
        orderbook_bids = get_hotcoinglobal_orderbook(symbol, False)
    elif exchange_sell == 'Cex.io':
        orderbook_bids = get_cexio_orderbook(symbol, False)
    elif exchange_sell == 'Binance':
        orderbook_bids = get_binance_orderbook(symbol, False)


#-------------------------------------------------------------------------------------------------------------------

    first_ask = float(orderbook_asks[0][0])
    first_bid = float(orderbook_bids[0][0])

    #SELLCAP 
    sellcap = first_ask + (first_bid - first_ask) * buffer

    #BUYCAP
    buycap = first_bid - (first_bid - first_ask) * buffer

    # Initialize sum varibales
    volume_asks = 0
    pricevolsum_asks = 0

    # Loop to go through ask orderbook starting at the best price
    for i in range(len(orderbook_asks)):
        # When price is greater than or equal to the buycap we exit the loop
        if float(orderbook_asks[i][0]) >= buycap:
            break
        volume_asks += float(orderbook_asks[i][1])
        pricevolsum_asks += float(orderbook_asks[i][0]) * float(orderbook_asks[i][1])
        avgprice_asks = pricevolsum_asks / volume_asks

    # Initialize sum varibales
    volume_bids = 0
    pricevolsum_bids = 0

    # Loop to go through the bid orderbook starting at the best price
    for i in range(len(orderbook_bids)):
        # When price is greater than or equal to the sellcap we exit the loop
        if float(orderbook_bids[i][0]) <= sellcap:
            break
        volume_bids += float(orderbook_bids[i][1])
        pricevolsum_bids += float(orderbook_bids[i][0]) * float(orderbook_bids[i][1])
        avgprice_bids = pricevolsum_bids / volume_bids

#-------------------------------------------------------------------------------------------------------------------
    # Initialize sum varibales
    vol_sum = 0
    pricevolsum = 0

    # Here we assign volume to be the bids one, we have avg sell price, now we look to calculate the avg buy price
    if volume_bids < volume_asks:
        volume = volume_bids
        sell_price = avgprice_bids
        vol_next = float(orderbook_asks[0][1])
        # loop that starts at 1 and uses it to sum i - 1 and look if i has exceeded our set volume
        # If not it continues to sum unit it does, then we take the difference of how much volume is left and add it at indexed price
        for i in range(1, len(orderbook_asks)):
            if vol_next > volume:
                volume_diff = volume - vol_sum
                if volume_diff > 0:
                    pricevolsum += float(orderbook_asks[i][0]) * volume_diff
                    vol_sum += volume_diff
                buy_price = float(pricevolsum / vol_sum)
                break
            else:
                vol_next += float(orderbook_asks[i][1])
                vol_sum += float(orderbook_asks[i - 1][1])
                pricevolsum += float(orderbook_asks[i - 1][0]) * float(orderbook_asks[i - 1][1])

                # I have this here because in the case that the list ends without exceeding the volume, then we still have a price
                buy_price = float(pricevolsum / vol_sum)

    # Here we assign volume to be the asks one, we have avg buy price, now we look to calculate the avg sell price
    if volume_bids >= volume_asks:
        volume = volume_asks
        buy_price = avgprice_asks
        vol_next = float(orderbook_bids[0][1])
        # loop that starts at 1 and uses it to sum i - 1 and look if i has exceeded our set volume
        # If not it continues to sum unit it does, then we take the difference of how much volume is left and add it at indexed price
        for i in range(1, len(orderbook_bids)):
            if vol_next > volume:
                volume_diff = volume - vol_sum
                if volume_diff > 0:
                    pricevolsum += float(orderbook_bids[i][0]) * volume_diff
                    vol_sum += volume_diff
                sell_price = float(pricevolsum / vol_sum)
                break
            else:
                vol_next += float(orderbook_bids[i][1])
                vol_sum += float(orderbook_bids[i - 1][1])
                pricevolsum += float(orderbook_bids[i - 1][0]) * float(orderbook_bids[i - 1][1])

                # I have this here because in the case that the list ends without exceeding the volume, then we still have a price
                sell_price = float(pricevolsum / vol_sum)



    info_dict = {'volume': volume, 'buy_price': buy_price, 'sell_price': sell_price,}

    return info_dict

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

#print(orderbook_info('IOTAUSDT', 'Hotcoin_Global', 'Kucoin'))