# Created by Sinatra Gunda 
# Created at 17/11/2026 10:53
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.db.models import QuerySet

from ifrs_metrics_engine.apps.project.models import Project, ProjectMember
from ifrs_metrics_engine.apps.workspace.models import Workspace, WorkspaceMember
from ifrs_metrics_engine.utils.choices import ACCESS_SCOPES


class WorkspaceQuerySet(QuerySet):

    def linked_users(self):
        pass

    # Returns all workspaces a user can view and the corresponding projects too .
    def workspaces_and_projects(self ,user_id):
        own_workspaces = Workspace.objects.filter(user_id=user_id)
        invited_workspaces = WorkspaceMember.objects.filter(user_id=user_id)

        for w in own_workspaces:
            own_workspaces.projects = Project.objects.filter(workspace_id=w.workspace_id)

        for w in invited_workspaces:
            workspace = w.workspace
            access_scope = workspace.access_scope
            w.projects = Project.objects.filter(workspace_id=w.workspace_id)


        assigned_projects = ProjectMember.objects.filter(user_id=user_id)
        assigned_projects = [a.project for a in assigned_projects]




