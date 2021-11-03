import requests
import telebot
from standard_request_data import UrlParametersKeys, ERROR_TYPES
from bot_config import bot_data
import json
from bot_src.tokens import BotTokens


bot = telebot.TeleBot(BotTokens.BOT_TOKEN.value)  # creating telegram bot

BTN_TEXTS = {'Find Nearest Town': 'nearest_settlement/',
             'Find Nearest Station': 'nearest_stations/'}

RADIUS_LIMIT = 50  # got from documentation
STATIONS_LIMIT = 5  # standard yandex option - limit = 100, but we don't need so much, so we will return only 5 for now


@bot.message_handler(commands=['start'])
def greetings(message):

    """
    Method of the bot's response to the user to the / start command

    Parameters:
    ----------
    message:
        User-submitted message
    """

    bot.send_message(message.chat.id, 'Hello!')
    bot.send_message(message.chat.id, 'Please, choose what do you want to find:')
    inline_keyboard = telebot.types.InlineKeyboardMarkup()
    btn_texts = ['Find Nearest Station', 'Find Nearest Town']
    for text in btn_texts:
        btn = telebot.types.InlineKeyboardButton(text=text, callback_data=BTN_TEXTS[text])
        inline_keyboard.add(btn)
    bot.send_message(message.chat.id, 'Select request type', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda call: call.data in [BTN_TEXTS.get(key) for key in BTN_TEXTS.keys()])
def find_nearest_object(call):

    """
    Method for finding nearest city to entered coordinates in !(latitude, longitude) - format
    """

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Delete previous", reply_markup=None)
    bot.send_message(call.message.chat.id, 'Enter latitude in real number format')
    bot.register_next_step_handler(call.message, get_latitude,
                                   url_data={UrlParametersKeys.URL_QUERY_TYPE.value: call.data})


def get_latitude(message, url_data: dict):
    txt = message.text
    try:
        long = float(txt)
        bot.send_message(message.chat.id, 'Great! Now, please, enter longitude in real number format')
        url_data.update({UrlParametersKeys.URL_LONGITUDE.value: str(long)})
        bot.register_next_step_handler(message, get_longitude,
                                       url_data=url_data)
    except ValueError:
        bot.send_message(message.chat.id, "Oops, incorrect format of input! Please, try again")
        bot.register_next_step_handler(message, get_latitude, url_data=url_data)


def get_longitude(message, url_data: dict):
    txt = message.text
    try:
        lat = float(txt)
        bot.send_message(message.chat.id, 'Ok, now you need to decide in which radius to look for the nearest station /'
                                          ' settlement.')
        bot.send_message(message.chat.id, 'Enter a real number from 1 to 50 (in km):')
        url_data.update({UrlParametersKeys.URL_LATITUDE.value: str(lat)})
        bot.register_next_step_handler(message, choose_distance, url_data=url_data)
    except ValueError:
        bot.send_message(message.chat.id, "Oopps, incorrect format of input! Please, try again")
        bot.register_next_step_handler(message, get_longitude, url_data=url_data)


def choose_distance(message, url_data: dict):
    txt = message.text
    try:
        distance = int(txt)
        if distance > RADIUS_LIMIT:
            bot.send_message(message.chat.id, "Radius of search is too big, please, reenter it")
            bot.register_next_step_handler(message, choose_distance, url_data=url_data)

        url_data.update({UrlParametersKeys.URL_RADIUS_KEY.value: str(distance)})
        result = create_data_request(url_data)
        msg = get_err_msg(result[1])

        if msg == ERROR_TYPES[200]:
            print_result_message(message, result[0])
        else:
            bot.send_message(message.chat.id, msg + "Please, restart your program!")

    except ValueError:
        bot.send_message(message.chat.id, "Oopps, incorrect format of input! Please, try again")
        bot.register_next_step_handler(message, choose_distance, url_data=url_data)


def create_data_request(url_data: dict):
    url = bot_data['api_url'] + 'yandex/'

    params = {
              # 'apikey': bot_data['api_key'],
              'query_type': url_data[UrlParametersKeys.URL_QUERY_TYPE.value],
              'lat': url_data[UrlParametersKeys.URL_LATITUDE.value],
              'lng': url_data[UrlParametersKeys.URL_LONGITUDE.value],
              'distance': url_data[UrlParametersKeys.URL_RADIUS_KEY.value]}

    if url_data[UrlParametersKeys.URL_QUERY_TYPE.value] == 'nearest_stations/':
        params.update({'limit': str(STATIONS_LIMIT)})

    response = requests.get(url, params=params)
    return [json.loads(response.content), response.status_code]


def print_nearest_object(obj_type: str, data: dict) -> str:
    return f"Nearest {obj_type} is: " + str(data['title']) + "\n" + \
           "Distance from entered coordinates: {} km".format(data['distance']) + "\n" + \
           f"{obj_type} latitude: {data['lat']}" + "\n" + \
           f"{obj_type} longitude: {data['lng']}" + "\n" + "Yandex code of settlement: {}".format(data['code'])


def print_result_message(message, response_data: dict):
    if 'pagination' in response_data:
        for i in range(int(response_data['pagination']['limit'])):
            msg = print_nearest_object('station', response_data['stations'][i])
            bot.send_message(message.chat.id, msg)
    else:
        msg = print_nearest_object('settlement', response_data)
        bot.send_message(message.chat.id, msg)


def get_err_msg(status_code: int):
    return ERROR_TYPES[status_code]


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, 'Hello!')
    bot.send_message(message.chat.id, 'Please, enter /start command to start working with bot')


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id, "I'm not a chat bot! Please, enter /help to start working with me")


bot.polling()
