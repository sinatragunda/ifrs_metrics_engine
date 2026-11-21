# Created by Sinatra Gunda 
# Created at 17/11/2026 10:53
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.apps import apps
from django.db.models import QuerySet

from ifrs_metrics_engine.utils.choices import ACCESS_SCOPES


class WorkspaceQuerySet(QuerySet):

    def linked_users(self):
        pass

    # Returns all workspaces a user can view and the corresponding projects too .
    def workspaces_and_projects(self ,user_id):

        own_workspaces = self.filter(user_id=user_id).prefetch_related("projects")

        Project = apps.get_model("ifrs_metrics_engine", "Project")
        WorkspaceMember = apps.get_model("ifrs_metrics_engine", "WorkspaceMember")
        ProjectMember = apps.get_model("ifrs_metrics_engine", "ProjectMember")

        invited_workspaces = WorkspaceMember.objects.filter(user_id=user_id)

        for w in invited_workspaces:
            workspace = w.workspace
            access_scope = w.access_scope
            w.projects = Project.objects.filter(workspace_id=w.workspace.workspace_id)


        assigned_projects = ProjectMember.objects.filter(user_id=user_id)
        assigned_projects = [a.project for a in assigned_projects]




