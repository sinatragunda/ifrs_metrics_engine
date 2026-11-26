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


class NotAuthenticated(APIException):
    status_code = 401
    default_detail = 'Not Authenticated'
    default_code = 'not_authenticated'

class NotAuthenticatedWithLoginRequirement(APIException):
    status_code = 401
    default_detail = 'Not Authenticated'
    default_code = 'not_authenticated'
    require_login = True

class ConflictError(APIException):
    status_code = 409
    default_detail = 'Conflict'
    default_code = 'conflict'

class NotFoundException(APIException):
    status_code = 404
    default_detail = 'Not Found'
    default_code = 'not_found'

class TokenExpiredException(APIException):
    status_code = 401
    default_detail = 'Token Expired'
    default_code = 'token_expired'