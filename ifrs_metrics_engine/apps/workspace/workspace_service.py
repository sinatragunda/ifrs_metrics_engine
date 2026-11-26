# Created by Sinatra Gunda 
# Created at 17/11/2026 09:45
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import json

from django.http import Http404
from starlette.status import HTTP_400_BAD_REQUEST

from ifrs_metrics_engine.apps.workspace.models import Workspace
from ifrs_metrics_engine.utils.annotations import atomic_op


class WorkspaceService:

    @atomic_op
    def create(self, workspace : Workspace):
        if workspace is None:
            raise HTTP_400_BAD_REQUEST
        workspace.save()
        return workspace

    def get_all_workspaces(self):
        return Workspace.objects.all()

    def get_workspace(self, workspace_id):
        return Workspace.objects.get(id=workspace_id)

    def get_workspace_by_user_id(self, user_id):
        return Workspace.objects.filter(user_id=user_id)

    def get_workspace_by_user_id_and_assigned_to(self, user_id):
        workspaces = self.get_workspace_by_user_id(user_id)

    def get_workspace_by_filter_key(self, **kwargs):
        return Workspace.objects.filter(**kwargs).first()
