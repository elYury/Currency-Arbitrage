
import requests

def send_discord(text):
    payload = {
        'content': str(text)
    }

    header = {
        'authorization': ' TYPE YOUR AUTHORIZATION CODE IN HERE'
    }

    r = requests.post("https://discord.com/api/v9/channels/1117711348747477075/messages", 
                        data=payload, headers=header)
