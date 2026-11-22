import uuid

from django.db import models
from docutils.parsers.rst.states import TYPE_CHECKING
from rest_framework import serializers


from ifrs_metrics_engine.apps.project.models import Project
from ifrs_metrics_engine.apps.workspace.models import Workspace
from ifrs_metrics_engine.utils import BaseEntity
from ifrs_metrics_engine.utils.choices import ACCESS_SCOPES, INVITATION_STATUS


# Create your models here.

class Invitation(BaseEntity):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    invitation_id = models.CharField(max_length=54, editable=False ,unique=True)
    token = models.CharField(max_length=128, unique=True)
    access_scope = models.CharField(max_length=32, choices=ACCESS_SCOPES.choices)
    status = models.CharField(max_length=32, choices=INVITATION_STATUS.choices, default=INVITATION_STATUS.PENDING)
    expires_at = models.DateTimeField()
    invited_by = models.ForeignKey("users.Users", on_delete=models.PROTECT, related_name="invitations_sent")
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "invitation"

    def __str__(self):
        return f"{self.email} ({self.status})"


class InvitationProject(BaseEntity):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, related_name="projects")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="invitations")

    class Meta:
        db_table = "invitation_project"
        constraints = [
            models.UniqueConstraint(fields=["invitation", "project"], name="unique_invitation_project"),
        ]

    def __str__(self):
        return f"invitation {self.invitation_id} -> project {self.project_id}"



class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation

        fields = '__all__'