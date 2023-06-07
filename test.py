
#reference
#https://developer-pro.bitmart.com/en/spot/#get-list-of-trading-pair-details

import requests

r = requests.get('https://api-cloud.bitmart.com/spot/v1/symbols/details')



info = r.json()
info = info['data']['symbols']
sym_list = []

for x in range(len(info)):
    if info[x]['quote_currency'] == 'USDT' and info[x]['trade_status'] == 'trading':
        sym_list.append(info[x]['symbol'])

print(sym_list)
