#lib for text to speech
import pyttsx3

#time and colored terminal text
from datetime import datetime
from termcolor import colored
#another time lib used for sleep
import time

#import configuration file
from config import minimum_difference, estimate_fees, pause_between_runs, pause_between_found_arbitages

#import calc order book
from order_book_calc import orderbook_info

#import tickers
from func_bybit import get_bybit_ticker
from func_kucoin import get_kucoin_ticker
from func_gateio import get_gateio_ticker
from func_hitbtc import get_hitbtc_ticker
from func_bitmart import get_bitmart_ticker
from func_kraken import get_kraken_ticker
from func_okx import get_okx_ticker
from func_hotcoinglobal import get_hotcoinglobal_ticker

# send to discord
from discord import send_discord

#import all the symbols from symobol list file
from sym_list import sym_list, ban_list

def main():
    #----------------------------------------------------------------------------------
    #initialize symbol values
    key = sym_list

    #------------------------------------------------------------------------------------------

    while True:
        # Time
        now = datetime.now()
        start_time = now.strftime("%H:%M:%S")

        # Counting success (s) and failiure of abri opportunities
        count = 0
        near_count = 0
        success_count = 0

        # Create a list of dicitonaries one for ticker values and one for exchange names each indexed at the corresponding number
        megalist = []
        exchange_list = []

        # RESULT OF FUNCTION LIST
        result_list = []

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

            megalist.append(get_kraken_ticker())
            exchange_list.append("Kraken")

            megalist.append(get_okx_ticker())
            exchange_list.append("OKX")

            megalist.append(get_hotcoinglobal_ticker())
            exchange_list.append("Hotcoin_Global")

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

                    # If same exchange is getting compared agaisnt itself then skip
                    if i == j:
                        continue

                    # Try to look at the price, but if one cant be sourced then skip
                    try:
                        ex1 = float(megalist[i][current_key])
                        ex2 = float(megalist[j][current_key])
                    except:
                    # If exchanges dont share the crypto then skip
                        continue

                    # Market price at exchange 1(sell exchange) is greater than market price at exchange 2(buy exchange)
                    if ex1 > ex2:

                        # Calc market price % difference
                        pcent_diff = ex1/ex2 * 100 - 100

                        # Filter by minimum % difference
                        if pcent_diff > minimum_difference and pcent_diff < 100: 

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
                                if str(error) == "local variable 'avgprice_asks' referenced before assignment":
                                    pass
                                else:
                                    print(f"Symbol: {current_key}, Buy Ex: {exchange_list[j]}, Sell Ex: {exchange_list[i]}")
                                    print(colored(f"{error}", "red"))
                                near_count += 1
                                continue

                            # Time when found
                            now = datetime.now()
                            current_time = now.strftime("%H:%M:%S")

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
                                #pyttsx3.speak(f"ARBITRAGE FOUND!")

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
                                
                                # Modify result list with found arbitrage
                                result = {'time' : current_time,
                                          'symbol' : current_key,
                                          'pcent_diff' : round(pcent_diff, 2), 
                                          'buy_exchange': exchange_list[j], 
                                          'sell_exchange': exchange_list[i],
                                          'volume': volume,
                                          'usdt_buy_amount' : usdt_buy_amount,
                                          'usdt_sell_amount' : usdt_sell_amount,
                                          'buy_price' : buy_price,
                                          'sell_price' : sell_price,
                                          'usdt_gain' : usdt_gain}
                                
                                result_list.append(result)

                                # Send message to discord
                                message = message1 + message2
                                send_discord(message)

                                # Increment counts for successful arbitrage and unsuccesful ones
                                success_count += 1

                                # Combat API Rate Limit
                                time.sleep(pause_between_found_arbitages)
                            else:
                                near_count += 1
                        else:
                            count += 1

        # Calculate end time and convert to int
        now = datetime.now()
        end_time = now.strftime("%H:%M:%S")

        start = datetime.strptime(start_time, '%H:%M:%S')
        end = datetime.strptime(end_time, '%H:%M:%S')

        #Print info on terminal
        print(colored(f'Unsuccesfull Arbies: {count}', 'light_red'))
        print(colored(f'Filtered Arbies: {near_count}', 'yellow'))
        print(colored(f"Successful Arbies: {success_count}\n", 'green'))
        print(colored(f'Compared {count + near_count + success_count} times\n', 'blue'))
        print(colored(f'Total time taken: {end - start}\n', 'magenta'))

        # Pause for X seconds 
        time.sleep(pause_between_runs)

main()