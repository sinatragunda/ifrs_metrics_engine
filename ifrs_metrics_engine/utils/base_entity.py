# Created by Sinatra Gunda 
# Created at 16/11/2026 14:00
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.db import models
from ifrs_metrics_engine.utils.constants import AUTH_USER_MODEL

class BaseEntity(models.Model):

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL ,on_delete=models.SET_NULL,null=True)

    class Meta:
        abstract = True