import requests
from dotenv import dotenv_values
import json


def generate_token():
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

    keys = dotenv_values('.env')
    oauth_token = keys['OAUTH_TOKEN']

    data = {"yandexPassportOauthToken": oauth_token}

    response = requests.post(url, json=data)
    cont = response.content
    answer = json.loads(cont)
    token = answer['iamToken']
    return token
