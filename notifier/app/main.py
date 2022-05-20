import sys
import json
import requests
from config import config

if __name__ == '__main__':

    print("Building the message...")

    url = config.SLACK_URL

    title = (f"Fresh Logs :warning:")
    message = ("O IT é uma casa a arder!")

    slack_data = {
        "username": "SuricataBot",
        "icon_emoji": ":monkey:",
        "attachments": [
            {
                "color": "#FF5F03",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }

    print("Sending...")

    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    print("Sent")