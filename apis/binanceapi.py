from binance.client import Client

apikey = "gKHnjT4bo0aZlqwVMp1XK25kXoVCQkoo8Iu9bNrqrwgwAbpP2m2WPJ0ruSvtJb1q"
secretkey = "0R5Y9IMzovnsb9cAmdH1EqsNFb5xLKqORPtV4lvAqFJW6iY53bd6soQ0KJtrf3S3"

clinet = Client(apikey,secretkey)
print("loggged in")

info = client.get_exchange_info()

for i in info:
    print(i)

