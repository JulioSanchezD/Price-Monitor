import requests

# Telegram parameters
bot_token: str = "1224634380:AAHZew1V_SLed0sxBxvYSUvHBD2iYz7mdo4"
bot_chatID: str = "1207170474"


def telegram_bot_sendtext(message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/' \
                'sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    return response.json()