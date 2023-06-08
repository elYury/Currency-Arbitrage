import requests

from func_bybit import get_bybit_orderbook
from func_bitmart import get_bitmart_orderbook
from func_gateio import get_gateio_orderbook
from func_hitbtc import get_hitbtc_orderbook
from func_kucoin import get_kucoin_orderbook

#bybit = get_bybit_orderbook(symbol, is the price we are looking for ask?)

def get_buy_cap(symbol, exchange_sell):
    if exchange_sell == 'Bybit':
        buycap = get_bybit_orderbook(symbol, False)
        buycap = buycap[0][0]

    elif exchange_sell == 'Bitmart':
        buycap = get_bitmart_orderbook(symbol, False)
        buycap = buycap[0]['price']

    elif exchange_sell == 'Gate.io':
        buycap = get_gateio_orderbook(symbol, False)
        buycap = buycap[0][0]
    
    elif exchange_sell == 'Hitbtc':
        buycap = get_hitbtc_orderbook(symbol, False)
        buycap = buycap[0][0]
    
    elif exchange_sell == 'Kucoin':
        buycap = get_kucoin_orderbook(symbol, False)
        buycap = buycap[0][0]

    return buycap

def get_sell_cap(symbol, exchange_buy):
    if exchange_buy == 'Bybit':
        sellcap = get_bybit_orderbook(symbol, True)
        sellcap = sellcap[0][0]

    elif exchange_buy == 'Bitmart':
        sellcap = get_bitmart_orderbook(symbol, True)
        sellcap = sellcap[0]['price']
    
    elif exchange_buy == 'Gate.io':
        sellcap = get_gateio_orderbook(symbol, True)
        sellcap = sellcap[0][0]

    elif exchange_buy == 'Hitbtc':
        sellcap = get_hitbtc_orderbook(symbol, True)
        sellcap = sellcap[0][0]
    
    elif exchange_buy == 'Kucoin':
        sellcap = get_kucoin_orderbook(symbol, True)
        sellcap = sellcap[0][0]

    return sellcap


def get_max_volume_asks(symbol, exchange_buy, exchange_sell):
    #asks
    #request asks from orderbook at the exchange we are trying to buy crypto
    if exchange_buy == 'Bybit':
        orderbook = get_bybit_orderbook(symbol, True)
        volume = 0
        pricevolsum = 0
        buycap = get_buy_cap(symbol, exchange_sell)
        for i in range(len(orderbook)):
            volume += float(orderbook[i][1])
            pricevolsum += float(orderbook[i][0]) * float(orderbook[i][1])
            if orderbook[i][0] >= buycap:
                break
            
    elif exchange_buy == 'Bitmart':
        orderbook = get_bitmart_orderbook(symbol, True)
        volume = 0
        pricevolsum = 0
        buycap = get_buy_cap(symbol, exchange_sell)
        for i in range(len(orderbook)):
            volume += float(orderbook[i]['amount'])
            pricevolsum += float(orderbook[i]['price']) * float(orderbook[i]['amount'])
            if orderbook[i]['price'] >= buycap:
                break

    elif exchange_buy == 'Gate.io':
        orderbook = get_gateio_orderbook(symbol, True)
        volume = 0
        pricevolsum = 0
        buycap = get_buy_cap(symbol, exchange_sell)
        for i in range(len(orderbook)):
            volume += float(orderbook[i][1])
            pricevolsum += float(orderbook[i][0]) * float(orderbook[i][1])
            if orderbook[i][0] >= buycap:
                break

    elif exchange_buy == 'Hitbtc':
        orderbook = get_hitbtc_orderbook(symbol, True)
        volume = 0
        pricevolsum = 0
        buycap = get_buy_cap(symbol, exchange_sell)
        for i in range(len(orderbook)):
            volume += float(orderbook[i][1])
            pricevolsum += float(orderbook[i][0]) * float(orderbook[i][1])
            if orderbook[i][0] >= buycap:
                break 

    elif exchange_buy == 'Kucoin':
        orderbook = get_kucoin_orderbook(symbol, True)
        volume = 0
        pricevolsum = 0
        buycap = get_buy_cap(symbol, exchange_sell)
        for i in range(len(orderbook)):
            volume += float(orderbook[i][1])
            pricevolsum += float(orderbook[i][0]) * float(orderbook[i][1])
            if orderbook[i][0] >= buycap:
                break     

    avgprice = float(pricevolsum / volume)
    tmpdict = {'avgprice': avgprice, 'volume': volume}
    return tmpdict


def get_max_volume_bids(symbol, exchange_buy, exchange_sell):
    #bids
    #request bids from orderbook at the exchange we are trying to sell crypto

    if exchange_sell == 'Bybit':
        orderbook = get_bybit_orderbook(symbol, False)
        volume = 0
        pricevolsum = 0
        sellcap = get_sell_cap(symbol, exchange_buy)
        for i in range(len(orderbook)):
            volume += float(orderbook[i][1])
            pricevolsum += float(orderbook[i][0]) * float(orderbook[i][1])
            if orderbook[i][0] <= sellcap:
                break

    elif exchange_sell == 'Bitmart':
        orderbook = get_bitmart_orderbook(symbol, False)
        volume = 0
        pricevolsum = 0
        sellcap = get_sell_cap(symbol, exchange_buy)
        for i in range(len(orderbook)):
            volume += float(orderbook[i]['amount'])
            pricevolsum += float(orderbook[i]['price']) * float(orderbook[i]['amount'])
            if orderbook[i]['price'] <= sellcap:
                break

    elif exchange_sell == 'Gate.io':
        orderbook = get_gateio_orderbook(symbol, False)
        volume = 0
        pricevolsum = 0
        sellcap = get_sell_cap(symbol, exchange_buy)
        for i in range(len(orderbook)):
            volume += float(orderbook[i][1])
            pricevolsum += float(orderbook[i][0]) * float(orderbook[i][1])
            if orderbook[i][0] <= sellcap:
                break

    elif exchange_sell == 'Hitbtc':
        orderbook = get_hitbtc_orderbook(symbol, False)
        volume = 0
        pricevolsum = 0
        sellcap = get_sell_cap(symbol, exchange_buy)
        for i in range(len(orderbook)):
            volume += float(orderbook[i][1])
            pricevolsum += float(orderbook[i][0]) * float(orderbook[i][1])
            if orderbook[i][0] <= sellcap:
                break

    elif exchange_sell == 'Kucoin':
        orderbook = get_kucoin_orderbook(symbol, False)
        volume = 0
        pricevolsum = 0
        sellcap = get_sell_cap(symbol, exchange_buy)
        for i in range(len(orderbook)):
            volume += float(orderbook[i][1])
            pricevolsum += float(orderbook[i][0]) * float(orderbook[i][1])
            if orderbook[i][0] <= sellcap:
                break

    avgprice = float(pricevolsum / volume)
    tmpdict = {'avgprice': avgprice, 'volume': volume}
    return tmpdict

def call_order_book(symbol, exchange_buy, exchange_sell):
    dictask = get_max_volume_asks(symbol, exchange_buy, exchange_sell)
    dictbid = get_max_volume_bids(symbol, exchange_buy, exchange_sell)
    tmpdict = {'infoask': dictask, 'infobid': dictask}
    return tmpdict


def orderbook_info(symbol, exchange_buy, exchange_sell):
    infodict = call_order_book(symbol, exchange_buy, exchange_sell)
    if infodict['infoask']['volume'] > infodict['infobid']['volume']:
        return infodict['infobid']
    else:
        return infodict['infoask']


#print(get_max_volume_bids())
#print(get_max_volume_asks())