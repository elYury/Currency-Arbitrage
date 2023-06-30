#lib for text to speech
import pyttsx3

#time and colored terminal text
from datetime import datetime
from termcolor import colored
#another time lib used for sleep
import time

#import configuration file
from config import minimum_difference, minimum_usdt_amount, pause_between_runs, txt_to_speech, ban_list, balance, takers

#import other fuctions
from order_book_calc import orderbook_info
from deposit_withdraw_calc import get_deposit, get_withdrawal, get_link

#import tickers
from func_bybit import get_bybit_ticker#, get_bybit_link
from func_kucoin import get_kucoin_ticker#, get_kucoin_link
from func_gateio import get_gateio_ticker#, get_gateio_link
from func_hitbtc import get_hitbtc_ticker#, get_hitbtc_link
from func_bitmart import get_bitmart_ticker#, get_bitmart_link
from func_kraken import get_kraken_ticker#, get_kraken_link
from func_okx import get_okx_ticker#, get_okx_link
from func_hotcoinglobal import get_hotcoinglobal_ticker#, hotcoinglobal_link
from func_cexio import get_cexio_ticker#, get_cexio_link
from func_binance import get_binance_ticker#, get_binance_link

# send to discord
from discord import send_discord

#import all the symbols from symobol list file
from sym_list import sym_list

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

            megalist.append(get_cexio_ticker())
            exchange_list.append("Cex.io")

            megalist.append(get_binance_ticker())
            exchange_list.append("Binance")

            print(colored('\nTickers loaded successfully\n', 'green'))

        except Exception as error:
            print(colored('\nTickers NOT loaded\n', 'red'))
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

                            # Skip Ban List
                            skip = False
                            for n in range(len(ban_list)):
                                if current_key == ban_list[n]['symbol'] and exchange_list[j] == ban_list[n]['exchange_buy'] and exchange_list[i] == ban_list[n]['exchange_sell']:
                                    print(colored(f"Banned item bypassed", 'light_blue'))
                                    near_count += 1
                                    skip = True
                                    break
                            if skip:
                                continue

                            # Try fetch the orderbook info values if it fails then skip to the next symbol
                            # It can fail quite often because there might not be arbi opportunities when looking at
                            # bids and asks, but there is one when looking at market price
                            try:
                                # params (symbol, buy exchange, sell exchange)
                                print(colored(f"Fetching Orderbook info: {current_key}, {exchange_list[j]}, {exchange_list[i]}", 'light_blue'))
                                orderinfo = orderbook_info(current_key, exchange_list[j], exchange_list[i])
                            except Exception as error:
                                # The 'local variable 'avgprice_asks' or 'avgprice_bids' referenced before assignment' error
                                # happens when there is a market price difference, but there is no abri opportunity
                                # because orderbook values are not correct and there is no money to be made
                                if str(error) == "local variable 'avgprice_asks' referenced before assignment":
                                    pass
                                else:
                                    print(f"Orderbook failed: {current_key}, {exchange_list[j]}, {exchange_list[i]}")
                                    print(colored(f"{error}", "red"))
                                near_count += 1
                                continue

                            # If we have the ability to detect if the symbol is not withrdawable or despositable then skip
                            try:
                                print(colored(f"Getting Deposit and withdrawal info: {current_key}, {exchange_list[j]}, {exchange_list[i]}", 'light_blue'))
                                withdraw = get_withdrawal(current_key, exchange_list[j])
                                deposit = get_deposit(current_key, exchange_list[i])
                            except Exception as deposit_withdraw_error:
                                print(f"Deposit and withdrawal info failed: {current_key}, {exchange_list[j]}, {exchange_list[i]}")
                                print(colored(f"{deposit_withdraw_error}", "red"))

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
                            takers_fee = round(sell_price * (float(volume) * takers[exchange_list[j]]/100 + float(volume) * takers[exchange_list[i]]/100), 2)

                            # Estimate profit basaed on balance ------ balance_buy_amount = balance
                            if usdt_buy_amount > balance:
                                balance_volume = str(balance / buy_price)
                                balance_sell_amount = str(float(balance_volume) * sell_price)
                                balance_usdt_gain = str(round(float(balance_sell_amount) - balance, 2))
                                balance_takers_fee = str(round(sell_price * (float(balance_volume) * takers[exchange_list[j]]/100 + float(balance_volume) * takers[exchange_list[i]]/100), 2))
                            else:
                                balance_volume = '-'
                                balance_sell_amount = '-'
                                balance_usdt_gain = 'Balance higher than buy amount'
                                balance_takers_fee = '-'

                            # Get symbol base ex. get BTC from BTCUSDT
                            currency_base = current_key.replace("USDT","")

                            # Declare variables
                            withdraw_networks = []
                            deposit_networks = []
                            withdraw_available = False                            
                            deposit_available = False                               

                            # Loop through diesposit and withdraw data and assign it to our list + see if deposit and withdraw available
                            for i in range(len(withdraw)):
                                withdraw_networks.append({withdraw[i]['network']:[withdraw[i]['fee'], withdraw[i]['pcent_fee']]})
                                if withdraw[i]['available']:
                                    withdraw_available = True
                            
                            for i in range(len(deposit)):
                                deposit_networks.append(deposit[i]['network'])
                                if deposit[i]['available']:
                                    deposit_available = True

                            # Gain larger than minimum amount 
                            if usdt_gain > minimum_usdt_amount and deposit_available and withdraw_available:

                                # Get links to exchange dashboard
                                buy_link = get_link(exchange_list[j], current_key)
                                sell_link = get_link(exchange_list[i], current_key)

                                # Text to speech
                                if txt_to_speech == True:
                                    pyttsx3.speak(f"ARBITRAGE FOUND!")

                                # Discord message
                                message1 = ("__**ARBITRAGE FOUND at " + str(current_time) + '**__\n' 
                                        + '**' + current_key + '**' + ' ' + str(round(pcent_diff, 2)) + '%\n' 
                                        + '\n' + '**BUY: ' + str(volume) + ' ' + currency_base + ' on ' 
                                        + exchange_list[j] + ', SELL on ' + exchange_list[i] + '**\n')
                                
                                message2 = ('``BUY ' + str(usdt_buy_amount) + ' USDT of ' + currency_base 
                                        + ' at ' + exchange_list[j] + ' Average buy price: ' + str(buy_price) 
                                        + ' USDT\n' + 'SELL ' + str(usdt_sell_amount) + ' USDT ' + 'at ' 
                                        + exchange_list[i] + ' Average sell price: ' + str(sell_price) 
                                        + ' USDT``\n' + 'Gain:** ' + str(usdt_gain) + "** USDT Taker's fees:** " 
                                        + str(takers_fee) + ' USDT**\n')
                                
                                message3 = ("\nBalance: " + str(balance) + ' USDT' + "\n**Buy: " + balance_volume + " " + currency_base 
                                            + '**\nEstimate gain based on balance:** ' + balance_usdt_gain + " USDT**\n"
                                            + "Balance taker's fees:** " + balance_takers_fee + " USDT**\n")

                                message4 = ("\n**Networks**\n``Withdrawal networks and fees: " + str(withdraw_networks) 
                                            + "\nDesposit networks: " + str(deposit_networks) + "``\n")
                                
                                message5 = "\n**Links:**\nBuy Exchange: " + buy_link + '\nSell Exchange: ' + sell_link
                                message6 = "\n---------------------------------------------------------"

                                # Append result list with found arbitrage
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
                                            'usdt_gain' : usdt_gain,
                                            'withdraw_networks' : withdraw_networks,
                                            'deposit_networks': deposit_networks}
                                
                                result_list.append(result)

                                # Send message to discord
                                message = message1 + message2 + message3 + message4 + message5 + message6
                                send_discord(message)

                                # Increment counts for successful arbitrage and unsuccesful ones
                                success_count += 1

                                # Combat API Rate Limit
                                print(colored('Arbitrage found', 'green'))
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
        print(colored(f'\nUnsuccesfull Arbies: {count}', 'light_red'))
        print(colored(f'Filtered Arbies: {near_count}', 'yellow'))
        print(colored(f"Successful Arbies: {success_count}\n", 'green'))
        print(colored(f'Compared {count + near_count + success_count} times\n', 'blue'))
        print(colored(f'Total time taken: {end - start}\n', 'magenta'))

        # Pause for X seconds
        print('Paused')
        time.sleep(pause_between_runs)
        print('Unpaused')

main()