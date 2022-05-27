import sys
import json
import time
import requests
from config import config
from os.path import exists
from itertools import islice

def send_message(url, data):
    byte_length = str(sys.getsizeof(data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

def send_error_message(url, msg):
    title = (f":warning: Suricata Error :warning:")
    message = (msg)

    data = {
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

    send_message(url, data)

def get_slack_data(title, message, channel):
    return {
        "username": "SuricataBot",
        "icon_emoji": ":monkey:",
        "channel" : channel,
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

def get_current_line():
    f = open("./current_line.txt", "r")    
    line = f.read()
    f.close()

    if line.isdecimal():
        return int(line)
    return 0


if __name__ == '__main__':

    url = config.SLACK_URL

    if not exists(config.SURICATA_LOCATION):
        send_error_message(url, "Logs file not found")
        exit(1)

    current_line = 0
    if exists("current_line.txt"):
        current_line = get_current_line()

    lines_total = sum (1 for _ in open(config.SURICATA_LOCATION))
    with open(config.SURICATA_LOCATION) as f:
        alerts = json.loads(
            '['+','.join(list(
                islice(f, current_line, 1000)
            ))+']'
        )

    sev_1 = []
    sev_2 = []
    sev_3 = []
    sev_4 = []

    for alert in alerts:
        try:
            if alert["proto"] == "TCP":
                if alert["alert"]["severity"] == 1:
                    sev_1.append(json.dumps(alert, indent=4))
                elif alert["alert"]["severity"] == 2:
                    sev_2.append(json.dumps(alert, indent=4))
                elif alert["alert"]["severity"] == 3:
                    sev_3.append(json.dumps(alert, indent=4))
                elif alert["alert"]["severity"] == 4:
                    sev_4.append(json.dumps(alert, indent=4))
        except KeyError:
            continue

    # SEVERITY 1
    if len(sev_1) != 0:
        for alert in sev_1:
            title = (f"Fresh Logs")
            message = alert
            send_message(url, get_slack_data(title, message, config.SLACK_SEV1))
            time.sleep(1)

    # SEVERITY 2
    if len(sev_2) != 0:
        for alert in sev_2:
            title = (f"Fresh Logs")
            message = alert
            send_message(url, get_slack_data(title, message, config.SLACK_SEV2))
            time.sleep(1)

    # SEVERITY 3
    if len(sev_3) != 0:
        for alert in sev_3:
            title = (f"Fresh Logs")
            message = alert
            send_message(url, get_slack_data(title, message, config.SLACK_SEV3))
            time.sleep(1)

    # SEVERITY 4
    if len(sev_4) != 0:
        for alert in sev_4:
            title = (f"Fresh Logs")
            message = alert
            send_message(url, get_slack_data(title, message, config.SLACK_SEV4))
            time.sleep(1)

    f = open("./current_line.txt", "w")
    f.write(lines_total)
    f.close()
