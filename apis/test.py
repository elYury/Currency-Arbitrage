import requests
import json

bybit = requests.get("https://api-testnet.bybit.com/v2/public/tickers")
e = bybit.json()

latest_price = []

for pair in e['result']:
    symbol = (pair['symbol'])
    price = (pair['last_price'])
    case = {symbol : price}
    latest_price.append(case)

print(latest_price)
