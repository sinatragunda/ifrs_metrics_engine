# Created by Sinatra Gunda 
# Created at 22/11/2026 03:49
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    print("are we handling this exception")

    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'status': response.status_code,
            'errors': getattr(exc ,'default_code' ,'error'),
            'message': response.data.get('message',str(exc))
        }

    return response
