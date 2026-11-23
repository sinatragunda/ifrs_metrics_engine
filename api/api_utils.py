# Created by Sinatra Gunda 
# Created at 22/11/2026 02:16
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.http import JsonResponse
from rest_framework.serializers import ModelSerializer


def json_response(model : ModelSerializer ,status):
    if model:
        return JsonResponse(data=model.data,safe=False ,status=status)
    return JsonResponse(safe=False ,status=status)