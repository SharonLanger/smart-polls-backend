import json
from configparser import RawConfigParser
import requests

config = RawConfigParser()
config.read('profile-dev.properties')
telegram_prefix = 'https://api.telegram.org/bot'
telegram_token = config.get('DatabaseSection', 'telegram_bot_token')
telegram_HTTP_API = telegram_prefix + telegram_token


class InlineKeyboard:
    class InlineKeyboardElement:
        def __init__(self, text, callback_data):
            self.text = text
            self.callback_data = callback_data

    inline_keyboard = []


def send_poll_telegram(poll_id, poll_text, answers, chat_id):
    """
    Send the poll to the telegram bot

    :param poll_id: Poll to send
    :param poll_text: Text of the poll used by the bot
    :param answers: List of options(concatenated by &)
    :param chat_id: Telegram chat_id of the user

    :return:
        response from the bot.
    """
    url = telegram_HTTP_API + "sendMessage"
    headers = {'Content-Type': 'application/json'}
    markup = build_reply_markup(poll_id, answers)
    payload = {
        'chat_id': chat_id,
        'text': poll_text,
        'reply_markup': markup}

    res = requests.post(url, headers=headers, params=payload)

    return res


def build_reply_markup(poll_id, answers):
    """
    Gets the poll and the answer options and builds the InlineKeyboard in the telegram format.
    Note: Every button in the keyboard holds the url that will be triggered once the button is clicked in the telegram bot

    :param poll_id: Poll build for
    :param answers: List of options(concatenated by &)

    :return:
        InlineKeyboard in a telegram format for the poll.
    """
    markdown = InlineKeyboard()
    for i, ans in enumerate(answers.split('&')):
        markdown_element = InlineKeyboard.InlineKeyboardElement(ans, str(poll_id) + "&" + str(ans))
        markdown.inline_keyboard.append(markdown_element)
    markdown_string = "{\"inline_keyboard\":["
    for i, itr in enumerate(markdown.inline_keyboard):
        if i != 0:
            markdown_string += ","
        json_str = json.dumps(itr.__dict__)
        markdown_string += "[" + json_str + "]"
    markdown_string += "]}"
    print(markdown_string)
    InlineKeyboard.inline_keyboard.clear()
    return markdown_string
