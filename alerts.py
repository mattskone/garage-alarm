import requests
import config


def trigger_alert():
    url = config.ALERT_URL.format(config.ALERT_NAME, config.ALERT_KEY)
    response = requests.post(url)
    response.raise_for_status()

