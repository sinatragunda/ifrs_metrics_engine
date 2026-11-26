import email

from django.db.models import Choices
from rest_framework import serializers
from django.db import models

from ifrs_metrics_engine.apps.workspace.workspace_query_set import WorkspaceQuerySet
from ifrs_metrics_engine.utils import BaseEntity
from ifrs_metrics_engine.utils.choices import ACCESS_SCOPES, IFRS_STANDARD, INVITATION_STATUS
from ifrs_metrics_engine.utils.context_util import generate_model_id


class Workspace(BaseEntity):
    name = models.CharField(null=False)
    workspace_id = models.CharField(null=False ,default=generate_model_id('workspace') ,unique=True)
    user_id = models.CharField() # this is an external user id from our external auth system .

    objects = WorkspaceQuerySet.as_manager()
    db_table = 'workspace'


class WorkspaceSerializer(serializers.ModelSerializer):
    access_scopes = serializers.ChoiceField(choices=ACCESS_SCOPES.choices, default=ACCESS_SCOPES.ADMIN)
    class Meta:
        model = Workspace
        fields = '__all__'

    def get_access_scopes(self):
        return ACCESS_SCOPES.ADMIN


class WorkspaceMember(BaseEntity):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="workspace_memberships" ,null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="members")
    access_scope = models.CharField(max_length=32, choices=ACCESS_SCOPES.choices)

    class Meta:
        db_table = "workspace_member"
        constraints = [
            models.UniqueConstraint(fields=["user", "workspace"], name="unique_workspace_member"),
        ]

    def __str__(self):
        return f"{self.user_id} @ workspace {self.workspace_id}"


class WorkspaceMemberSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()

    def get_email(self ,obj):
        return self.context.get("email")

    class Meta:
        model = WorkspaceMember
        fields = '__all__'




