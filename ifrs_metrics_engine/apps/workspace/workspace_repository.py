# Created by Sinatra Gunda 
# Created at 17/11/2026 09:45
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.http import Http404
from starlette.status import HTTP_400_BAD_REQUEST

from ifrs_metrics_engine.apps.workspace.models import Workspace

class WorkspaceRepository:

    def save(self, workspace):
        if not workspace:
            raise HTTP_400_BAD_REQUEST
        return workspace.save()

    def get_all_workspaces(self):
        return Workspace.objects.all()

    def get_workspace(self, workspace_id):
        return Workspace.objects.get(id=workspace_id)

    def get_workspace_by_user_id(self, user_id):
        return Workspace.objects.filter(user_id=user_id)