import time
import pyttsx3
#import pywhatkit

from datetime import datetime
from termcolor import colored

#import symbols and calc liquidity
from func_bybit import get_bybit_symbols
from order_book_calc import orderbook_info


#import tickers
from func_bybit import get_bybit_ticker
from func_kucoin import get_kucoin_ticker
from func_gateio import get_gateio_ticker
from func_hitbtc import get_hitbtc_ticker
from func_bitmart import get_bitmart_ticker

from func_discord import send_discord
import json

#import all the symbols from json file
from sym_list import sym_list
from sym_list import ban_list
key = sym_list
#with open('sym_list.json') as json_file:
    #key = json.load(json_file)

#initialize values
#minimum % difference for arbitrage
minimum_difference = 2.5
#estimate for all fees in USDT
estimatefees = 5
#isstart
isstart = True
#------------------------------------------------------------------------------------------

while True:
    #run code every 60seconds unless its the first time we are running it
    if isstart == False:
        time.sleep(30)

    #time
    currentDateAndTime = datetime.now()
    currenthour = currentDateAndTime.strftime("%H")
    currentminute = currentDateAndTime.strftime("%M")
    
    #counting success (s) and failiure of abri opportunities
    count = 0
    scount = 0

    #create a list of dicitonaries "yes im doing it manually because its easier" ctl c is king
    megalist = []
    exchange_list = []

    megalist.append(get_bybit_ticker())
    exchange_list.append("Bybit")

    megalist.append(get_kucoin_ticker())
    exchange_list.append("Kucoin")

    megalist.append(get_gateio_ticker())
    exchange_list.append("Gate.io")

    megalist.append(get_hitbtc_ticker())
    exchange_list.append("Hitbtc")

    megalist.append(get_bitmart_ticker())
    exchange_list.append("Bitmart")

    print('')
    print('loading...')
    print('')

    #time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    #delete data in the text file
    open('Arbitrage.txt', 'w').close()
    open('difference.txt', 'w').close()

    #open file
    difffile = open('difference.txt', 'w')

    arbifile = open('Arbitrage.txt', 'w')
    arbifile.write("Arbitrage Opportunities:\n")
    arbifile.write('-' * 50 + '\n')
    arbifile.write('\n')

    # calculation looping over each key on each exchange
    for x in range(len(key)):
        current_key = key[x]
        for i in range(len(megalist)):
            for j in range(len(megalist)):
                #if same exchange is getting compared agaisnt itself then skip
                if i == j:
                    continue
                #try to look at the price, but if one cant be sourced then skip
                try:
                    ex1 = float(megalist[i][current_key])
                    ex2 = float(megalist[j][current_key])
                except:
                    continue
                # calc %
                if ex1 > ex2:
                    x = ex1/ex2 * 100 - 100
                    if x > minimum_difference: 
                        if current_key in ban_list:
                            continue
                            #pass

                        difffile.write(f"Difference in {current_key} of {x}% B: {exchange_list[j]}, S:{exchange_list[i]}\n")
                        
                        #try fetch the orderbook data if it fails then skip to the next symbol
                        try:
                            orderinfo = orderbook_info(current_key, exchange_list[j], exchange_list[i])
                        except:
                            send_discord('**failed** to fetch order book for ' + current_key + ' at buy exchange ' + exchange_list[j] + ' and sell exchange '+ exchange_list[i])
                            continue
                        
                        #do all juicy calculations
                        volume = orderinfo['volume']
                        avgprice = orderinfo['avgprice']
                        currency_base = current_key.replace("USDT","")
                        ask_or_bid_fullyfilled = orderinfo['dicttype']
                        totalprice = avgprice * volume

                        #print(f"symbol{current_key}, B: {exchange_list[j]}, S:{exchange_list[i]}")

                        if ask_or_bid_fullyfilled == 'ask':
                            estimategain = round(ex1 * volume - totalprice, 2)

                        if ask_or_bid_fullyfilled == 'bid':
                            estimategain = round(totalprice - ex2 * volume, 2) 
                        
                        if estimategain > 5 + estimatefees:
                            ('$\n')
                            pyttsx3.speak(f"ARBITRAGE FOUND!")
                            arbifile.write(f"ARBITRAGE FOUND at {current_time}\n")
                            arbifile.write("")
                            arbifile.write(f"Gain: {round(x, 2)}%    Pair: {current_key}\n")
                            arbifile.write(f"BUY: {volume} {currency_base} on {exchange_list[j]}, SELL on {exchange_list[i]}\n")
                            arbifile.write('\n')
                            message1 = "__**ARBITRAGE FOUND at " + str(current_time) + '**__\n' + '**' + current_key + '**' + ' ' + str(round(x, 2)) + '%' + '\n' + '**BUY: ' + str(volume) + ' ' + currency_base + ' on ' + exchange_list[j] + ', SELL on ' + exchange_list[i] + '**\n'


                            if ask_or_bid_fullyfilled == 'ask':
                                arbifile.write(f'BUY {totalprice} USDT of {currency_base} at {exchange_list[j]} || Average price: {avgprice} USDT\n')
                                arbifile.write(f'SELL at {exchange_list[i]} || Market sell price: {ex1} USDT\n')
                                arbifile.write(f'Estimated gain: ' + str(estimategain))
                                arbifile.write(' USDT\n')
                                arbifile.write(f'Fill all orders until we CAP on the exchange we BUY at {exchange_list[i]}\n')

                                message2 = '``BUY ' + str(totalprice) + ' USDT of ' + currency_base + ' at ' + exchange_list[j] + ' Average price: ' + str(avgprice) + ' USDT\n' + 'SELL at ' + exchange_list[i] + ' Market sell price: ' +  str(ex1) + ' USDT``\n' + '**Estimated gain: ' + str(estimategain) + ' USDT**\n'
                                message3 = '`CAP on BUY ' + exchange_list[i] + '`'

                            if ask_or_bid_fullyfilled == 'bid':

                                arbifile.write(f'BUY at {exchange_list[j]} || Market buy price: {ex2} USDT\n')
                                arbifile.write(f'SELL {totalprice} USDT of {currency_base} at {exchange_list[i]} Average price: {avgprice} USDT\n')
                                arbifile.write(f'Estimated gain: ' + str(estimategain))
                                arbifile.write(' USDT\n')
                                arbifile.write(f'Fill all orders until we CAP on the exchange we SELL at {exchange_list[j]}\n')

                                message2 = '``BUY at '+ exchange_list[j] + ' Market buy price: ' + str(ex2) +' USDT\n' + 'SELL ' + str(totalprice) + ' USDT of '+ currency_base + ' at '  + exchange_list[i] +' Average price: ' + str(avgprice) + ' USDT``\n' + '**Estimated gain: ' + str(estimategain) + " USDT**\n"
                                message3 = '`CAP on SELL ' + exchange_list[j] + '`'

                            arbifile.write('-' * 50 + '\n')

                            #send message to discord
                            message = message1 + message2 + message3
                            send_discord(message)

                            scount += 1
                        else:
                            count += 1
                    else:
                        count += 1

            
    arbifile.write(f"Arbi Opportunities: {scount} \n")
    arbifile.write(f"Unsuccesfull Arbies: {count} \n")
    arbifile.write('\n')
    arbifile.write('*NOTE: Market price not accurate measure of profit gain\n')
    arbifile.write('\n')
    arbifile.write(f"Last run at {current_time}\n")

    print(f"Arbi Opportunities: {scount} \n")
    print(f"Unsuccesfull Arbies: {count} \n")
    print(colored(f'completed scan at {current_time}', 'green'))
    print('')

    arbifile.close()
    difffile.close()
    isstart = False

