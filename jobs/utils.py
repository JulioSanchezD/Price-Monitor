import requests
import json
import os


with open(os.path.join(os.path.dirname(__file__), "telegram_parameters.json")) as f:
    telegram_params = json.load(f)


def telegram_bot_sendtext(message):
    send_text = 'https://api.telegram.org/bot' + telegram_params["bot_token"] + '/' \
                'sendMessage?chat_id=' + telegram_params["bot_chatID"] + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    return response.json()


if __name__ == "__main__":
    telegram_bot_sendtext("hola julio esto es una prueba")