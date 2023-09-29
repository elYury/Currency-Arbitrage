
# https://discord.com/api/v9/channels/1117711348747477075/messages

import requests

def send_discord(text):
    payload = {
        'content': str(text)
    }

    header = {
        'authorization': 'security is number one priority'
    }

    r = requests.post("https://discord.com/api/v9/channels/1117711348747477075/messages", 
                        data=payload, headers=header)
