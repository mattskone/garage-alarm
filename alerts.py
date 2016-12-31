import requests
import config


def trigger_alert():
    url = config.ALERT_URL.format(event=config.ALERT_NAME,
                                  key=config.ALERT_KEY)
    response = requests.post(url)
    response.raise_for_status()

