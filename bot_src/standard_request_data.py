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
