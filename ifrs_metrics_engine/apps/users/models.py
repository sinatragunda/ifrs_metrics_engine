import uuid

from django.db import models

from ifrs_metrics_engine.utils import BaseEntity

# Create your models here.

class Users(BaseEntity):
    auth_user_id = models.CharField(editable=False ,unique=True)
    display_name = models.CharField(max_length=100)
    email = models.CharField(editable=False ,max_length=100)
    username = models.CharField(editable=False ,max_length=100)
    db_table = 'users'