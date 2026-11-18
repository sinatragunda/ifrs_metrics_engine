from rest_framework import serializers
from django.db import models

from ifrs_metrics_engine.apps.workspace.workspace_query_set import WorkspaceQuerySet
from ifrs_metrics_engine.utils import BaseEntity


# Create your models here.

class Workspace(BaseEntity):
    name = models.CharField()
    workspace_id = models.CharField()
    user_id = models.CharField() # this is an external user id from our external auth system .
    objects = WorkspaceQuerySet.as_manager()

    db_table = 'workspace'

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'
