
from django.db import models
from rest_framework import serializers

from ifrs_metrics_engine.apps.workspace.models import Workspace
from ifrs_metrics_engine.utils import BaseEntity
from ifrs_metrics_engine.utils.choices import IFRS_STANDARD

# Create your models here.
class Project(BaseEntity):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    ifrs_standard = models.CharField(max_length=32, choices=IFRS_STANDARD.choices)
    archived = models.BooleanField(default=False)

    class Meta:
        db_table = "project"

    def __str__(self):
        return self.name

class ProjectMember(BaseEntity):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="project_memberships")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")

    class Meta:
        db_table = "project_member"
        constraints = [
            models.UniqueConstraint(fields=["user", "project"], name="unique_project_member"),
        ]

    def __str__(self):
        return f"{self.user_id} @ project {self.project_id}"


class ProjectSerializer(serializers.ModelSerializer):
    access_scope = serializers.ChoiceField(choices  = IFRS_STANDARD.choices)
    class Meta:
        model = Project
        fields = '__all__'