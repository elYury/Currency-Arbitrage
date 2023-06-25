#lib for text to speech
import pyttsx3

#time and colored terminal text
from datetime import datetime
from termcolor import colored
#another time lib used for sleep
import time

#import calc order book
from order_book_calc import orderbook_info

#import tickers
from func_bybit import get_bybit_ticker
from func_kucoin import get_kucoin_ticker
from func_gateio import get_gateio_ticker
from func_hitbtc import get_hitbtc_ticker
from func_bitmart import get_bitmart_ticker

# send to discord
from func_discord import send_discord

#import all the symbols from symobol list file
from sym_list import sym_list
from sym_list import ban_list

def main():
    #----------------------------------------------------------------------------------
    #initialize values
    key = sym_list

    #minimum % difference for arbitrage
    minimum_difference = 2.5

    #estimate for all fees in USDT (used to filter unprofitable opportunities)
    estimate_fees = 20

    #------------------------------------------------------------------------------------------

    while True:
        #counting success (s) and failiure of abri opportunities
        count = 0
        success_count = 0

        #time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        #create a list of dicitonaries one for ticker values and one for exchange names each indexed at the corresponding number
        megalist = []
        exchange_list = []

        try:
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

            print(colored('Tickers loaded successfully\n', 'green'))

        except Exception as error:
            print(colored('Tickers NOT loaded\n', 'red'))
            print(error)

        # calculation looping over each key on each exchange
        for x in range(len(key)):
            current_key = key[x]

            # Loop through the first exchange in the megalist
            for i in range(len(megalist)):

                # Loop through the second exchange in the megalist
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

                    # Market price at exchange 1(sell exchange) is greater than market price at exchange 2(buy exchange)
                    if ex1 > ex2:

                        # Calc market price % difference
                        pcent_diff = ex1/ex2 * 100 - 100

                        # Filter by minimum % difference
                        if pcent_diff > minimum_difference: 

                            # Ban List
                            if current_key in ban_list:
                                continue
                            
                            # Try fetch the orderbook info values if it fails then skip to the next symbol
                            # It can fail quite often because there might not be arbi opportunities when looking at
                            # bids and asks, but there is one when looking at market price
                            try:
                                # params (symbol, buy exchange, sell exchange)
                                orderinfo = orderbook_info(current_key, exchange_list[j], exchange_list[i])
                            except Exception as error:
                                # The 'local variable 'avgprice_asks' or 'avgprice_bids' referenced before assignment' error
                                # happens when there is a market price difference, but there is no abri opportunity
                                # because orderbook values are not correct and there is no money to be made
                                print(error)
                                count += 1
                                continue
                            
                            # Assign values from order_book-calc function
                            volume = float(orderinfo['volume'])
                            buy_price = float(orderinfo['buy_price'])
                            sell_price = float(orderinfo['sell_price'])

                            # Estimate profit my friend ;)
                            usdt_buy_amount = buy_price * volume
                            usdt_sell_amount = sell_price * volume
                            usdt_gain = round(usdt_sell_amount - usdt_buy_amount, 2)

                            # GEt symbol base ex. get BTC from BTCUSDT
                            currency_base = current_key.replace("USDT","")

                            # Gain larger than fees
                            if usdt_gain > estimate_fees:

                                # Text to speech
                                pyttsx3.speak(f"ARBITRAGE FOUND!")

                                # Discord message
                                message1 = ("__**ARBITRAGE FOUND at " + str(current_time) + '**__\n' 
                                        + '**' + current_key + '**' + ' ' + str(round(pcent_diff, 2)) + '%' 
                                        + '\n' + '**BUY: ' + str(volume) + ' ' + currency_base + ' on ' 
                                        + exchange_list[j] + ', SELL on ' + exchange_list[i] + '**\n')
                                
                                message2 = ('``BUY ' + str(usdt_buy_amount) + ' USDT of ' + currency_base 
                                        + ' at ' + exchange_list[j] + ' Average buy price: ' + str(buy_price) 
                                        + ' USDT\n' + 'SELL ' + str(usdt_sell_amount) + ' USDT ' + 'at ' 
                                        + exchange_list[i] + ' Average sell price: ' + str(sell_price) 
                                        + ' USDT``\n' + '**Estimated gain: ' + str(usdt_gain) + ' USDT**\n')

                                # Send message to discord
                                message = message1 + message2
                                send_discord(message)

                                # Increment counts for successful arbitrage and unsuccesful ones
                                success_count += 1
                            else:
                                count += 1
                        else:
                            count += 1

        #Print info on terminal
        print(colored(f'Unsuccesfull Arbies: {count}', 'red'))
        print(colored(f"Arbi Opportunities: {success_count}\n", 'green'))
        print(colored(f'completed scan at {current_time}\n', 'blue'))

        # Pause for X seconds 
        time.sleep(30)

main()