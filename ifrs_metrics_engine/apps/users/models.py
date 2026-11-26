import uuid

from django.db import models
from rest_framework import serializers

from ifrs_metrics_engine.utils import BaseEntity

# Create your models here.

class Users(BaseEntity):
    auth_user_id = models.CharField(editable=False ,unique=True)
    display_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100 ,null=False)
    username = models.CharField(editable=False ,max_length=100 ,null=False)
    db_table = 'users'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'