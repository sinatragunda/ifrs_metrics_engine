# Created by Sinatra Gunda 
# Created at 17/11/2026 02:17
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_root(request, format=None):
    message = {
        'version': '1.0',
        'message': 'Hello World From IFRS Metrics Engine!',
        'developer': 'IFRS Metrics',
    }

    return JsonResponse(message, safe=False)