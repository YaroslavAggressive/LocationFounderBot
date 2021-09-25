from enum import Enum


class UrlParametersKeys(Enum):

    """

    """

    URL_APIKEY = 'apikey'
    URL_QUERY_TYPE = 'query'
    URL_LONGITUDE = 'lng'
    URL_LATITUDE = 'lat'
    URL_RADIUS_KEY = 'distance'


ERROR_TYPES = {404: "Error: Object with the code specified in the request was not found.",
               400: "Error: The request is invalid. Required parameters not specified.",
               200: "No error"}


# class QueryTypes(Enum):
#
#     """
#     Class of requests from one bot method to another for their interaction
#     """
#
#     QUERY_ROUTE = 'find_route'
#     QUERY_SCHEDULE = 'get_schedule'
#     QUERY_NEAR_TOWN = 'nearest_town'
#
#
# class YandexURLTypes(Enum):
#
#     """
#     Class with options for postfixes in requests for sending api schedules to Yandex
#     """
#
#     URL_ROUTE = 'search/'
#     URL_SCHEDULE = 'schedule/'
#     URL_NEAR_TOWN = 'nearest_settlement/'
#     URL_STATIONS_LIST = 'stations_list/'
#
#
# class Prefixes(Enum):
#
#     """
#     Class of prefixes that replace the search for elements with each new callback
#     """
#
#     CODE_PREFIX = 'yandex_code'
#     REGION_PREFIX = 'region'
#     SETTLEMENT_PREFIX = 'town'
#
#
# SUPPORTED_REGIONS = ['Пермский край', "Ленинградская область"]
# DEFAULT_COUNTRY = "Россия"
#
#
# @bot.callback_query_handler(func=lambda call: call.data in [e.value for e in YandexURLTypes])
# def choose_region(call):
#
#     """
#     Method for polling a user to create a search request for a train schedule
#     """
#
#     # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="", reply_markup=None)
#     request_data.append(call.data)  # added request postfix to Yandex api
#     bot.send_message(call.message.chat.id, 'You\'ve chosen train schedule finder! '
#                                            'Now, please, enter the region from which you plan to search for the path')
#     inline_keyboard = telebot.types.InlineKeyboardMarkup()
#     for region in SUPPORTED_REGIONS:
#         inline_keyboard.add(telebot.types.InlineKeyboardButton(text=region, callback_data=Prefixes.REGION_PREFIX.value
#                                                                                           + region))
#     bot.send_message(call.message.chat.id, text="Select departure region:", reply_markup=inline_keyboard)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith(Prefixes.REGION_PREFIX.value))
# def choose_town(call):
#
#     """
#     Method for getting a list of cities in the previously selected region
#     """
#
#     # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="", reply_markup=None)
#     request_data.append(call.data.rstrip(Prefixes.REGION_PREFIX.value))
#     # got the selected region from the last current element
#     list_of_towns = get_towns_list(DEFAULT_COUNTRY, call.data)
#     inline_keyboard = telebot.types.InlineKeyboardMarkup()
#     for settlement in list_of_towns:
#         chosen_cities.append(settlement['title'])  # to go to the next callback-function
#         inline_keyboard.add(telebot.types.InlineKeyboardButton(text=settlement['title'], callback_data=call.data.
#                                                                startswith(Prefixes.SETTLEMENT_PREFIX.value) + settlement['title']))
#     bot.send_message(call.message.chat.id, text="Select region settlement:", reply_markup=inline_keyboard)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith(Prefixes.SETTLEMENT_PREFIX.value))
# def choose_station(call):
#
#     """
#     Method of searching for transport hubs, from which you can arrive in the city or leave it
#     """
#
#     request_data.append(call.data.rstrip(Prefixes.SETTLEMENT_PREFIX.value))
#     bot.send_message(call.message.chat.id, 'The end is near! Please, choose your station for departure or arrival:')
#     towns = get_towns_list(DEFAULT_COUNTRY, request_data[1])
#     stations = []
#     for town in towns:
#         if town['title'] == call.data:
#             stations = town['stations']
#             break
#     inline_keyboard = telebot.types.InlineKeyboardMarkup()
#     for station in stations:
#         inline_keyboard.add(telebot.types.InlineKeyboardButton(text=station['title'],
#                                                                callback_data=Prefixes.CODE_PREFIX.value +
#                                                                              station['codes']['yandex_code']))
#
#     bot.send_message(call.message.chat.id, text="Select your station:", reply_markup=inline_keyboard)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith(Prefixes.CODE_PREFIX))
# def create_stations_request(call):
#
#     """
#     Method of searching for transport hubs, from which you can arrive in the city or leave it
#     """
#
#     request_data.append(call.data.rstrip(Prefixes.CODE_PREFIX.value))
#
#     request_params = {'apikey': bot_data['api_key'],
#                       }
#     bot.send_message()
#
#
# def get_towns_list(country: str, region: str) -> list:
#
#     """
#     Method of obtaining all settlements in the selected region
#     """
#
#     list_of_regions = get_regions_list(country)
#
#     for reg in list_of_regions:
#         if reg['title'] == region:
#             return [settlement for settlement in reg['settlements']][:MAX_ELEMENTS_COUNT]
#     return []
#
#
# def get_regions_list(country: str) -> list:
#
#     """
#     Method of obtaining all regions of the selected country (while the default is taken)
#     """
#
#     url = bot_data['api_url'] + YandexURLTypes.URL_STATIONS_LIST.value
#     response = requests.get(url, params={'apikey': bot_data['api_key'],
#                                          'format': 'json'})
#     response_data = json.loads(response.content)
#
#     for countr in response_data['countries']:
#         if countr['title'] == country:
#             return [region for region in countr['regions']]
#     return []
