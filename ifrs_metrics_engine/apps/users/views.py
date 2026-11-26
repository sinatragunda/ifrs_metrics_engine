from dependency_injector.wiring import inject, Provide
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

from api.api_utils import json_response
from boot_infrastructure.exceptions.custom_exceptions import BadRequestException
from ifrs_metrics_engine.apps.users.models import UserSerializer
from ifrs_metrics_engine.apps.users.user_service import UserService


# Create your views here.

@api_view(['POST' ,'GET'])
@inject
def user_root_view(request ,user_service : UserService = Provide['user-service']):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
         return create_user(request.data)

def create_user(request ,user_service : UserService):
     user_data = request.data
     if not user_data:
         raise BadRequestException("Invalid or empty user data")
     user = user_service.create_user_signup(user_data)
     print(type(user) ,user)

     #serializer = UserSerializer(user)
     return json_response(user ,status.HTTP_200_OK)