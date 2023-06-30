import requests
import json

api_key = "gKHnjT4bo0aZlqwVMp1XK25kXoVCQkoo8Iu9bNrqrwgwAbpP2m2WPJ0ruSvtJb1q"
api_secret = "0R5Y9IMzovnsb9cAmdH1EqsNFb5xLKqORPtV4lvAqFJW6iY53bd6soQ0KJtrf3S3"

url = 'https://apil.binance.com'
api_call = '/sapi/v1/capital/config/getall'
headers = {'content-type': 'application/json', 'X-MBX-APIKEY': api_key}

r = requests.get(url + api_call, headers=headers)
info = r.json()
print(info)