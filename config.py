
# CONFIGURATION OF ARBITRAGE BOT FILE
#_________________________________________________________________-

repeat = False
# Used to stop text to speech (False = no text to speech)
txt_to_speech = False

# Minimum difference between market prices when fetching ticker in order to identifiy potential arbitrage opportunities
# Measured in %
minimum_difference = 3

# Estimation of fees, the bot will not take arbitrage opportunities which yield a smaller return than the estimation of fees
# Measured in USDT
estimate_fees = 20

# Buffer changes the buy cap (-) and sell cap (+) by the given %
# Measured in decimal 0.1 = 10%, 0.9 = 90%, tu eres listo eh
buffer = 0.1

# Does exactly what you think
# Measured in seconds
pause_between_runs = 5

# Does exactly what you think in order not to hit the API rate limit (with 10 api calls per minuite maxium, 8sec is the min)
# Measured in seconds
pause_between_found_arbitages = 8

# SECTION FOR API KEYS, SECRETS, AND PASSCODES
#_________________________________________________________________-


