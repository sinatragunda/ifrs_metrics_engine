import uuid
from dataclasses import dataclass

from django.db import models
from rest_framework import serializers

from ifrs_metrics_engine.apps.workspace.models import Workspace
from ifrs_metrics_engine.utils import BaseEntity
from ifrs_metrics_engine.utils.choices import IFRS_STANDARD, ACCESS_SCOPES
from ifrs_metrics_engine.utils.context_util import generate_model_id


# Create your models here.
class Project(BaseEntity):

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255 ,null=False)
    ifrs_standard = models.CharField(max_length=32, choices=IFRS_STANDARD.choices ,null=False)
    archived = models.BooleanField(default=False)
    project_id = models.CharField(null=False, max_length=60 ,default=generate_model_id('project'))

    class Meta:
        db_table = "project"
        unique_together = (("created_by", "name"),)

    def __str__(self):
        return self.name

class ProjectMember(BaseEntity):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="project_memberships")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    access_scope = models.CharField(max_length=32, choices=ACCESS_SCOPES.choices ,default=ACCESS_SCOPES.ADMIN)

    class Meta:
        db_table = "project_member"
        constraints = [
            models.UniqueConstraint(fields=["user", "project"], name="unique_project_member"),
        ]

    def __str__(self):
        return f"{self.user_id} @ project {self.project_id}"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectResponseSerializer(serializers.ModelSerializer):
    ownerName = serializers.CharField(source="created_by.username", read_only=True)
    workspaceId = serializers.CharField(source="workspace.workspace_id", read_only=True)
    ifrsStandard = serializers.CharField(source="ifrs_standard", read_only=True)
    createdAt = serializers.DateTimeField(read_only=True ,source="created_at")
    ownerId = serializers.CharField(read_only=True ,source="created_by.auth_user_id")
    class Meta:
        model = Project
        fields = '__all__'


class ProjectTemplateSerializer(serializers.Serializer):

    ifrs_standards = serializers.SerializerMethodField()

    def get_ifrs_standards(self ,obj):
        values = IFRS_STANDARD.choices

        return [{
            'id': index ,
            'code':ifrs[0] ,
            'value':ifrs[1]
        }
        for index, ifrs in enumerate(values)]

@dataclass(frozen=True)
class ProjectsRequest:
    name : str
    standard : str
    workspaceId : str
    files : list[any]