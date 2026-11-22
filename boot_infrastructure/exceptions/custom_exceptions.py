# Created by Sinatra Gunda 
# Created at 22/11/2026 03:48
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    status_code = 400
    default_detail = 'Bad Request'
    default_code = 'bad_request'

class InternalServerError(APIException):
    status_code = 500
    default_detail = 'Internal Server Error'
    default_code = 'internal_server_error'