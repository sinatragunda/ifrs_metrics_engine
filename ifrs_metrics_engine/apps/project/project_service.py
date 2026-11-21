# Created by Sinatra Gunda 
# Created at 19/11/2026 09:36
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from dataclasses import dataclass

from dependency_injector.wiring import inject, Provide
from django.db import transaction

from ifrs_metrics_engine.apps.project.models import Project
from ifrs_metrics_engine.apps.workspace.workspace_service import WorkspaceService
from ifrs_metrics_engine.utils.annotations import atomic_op
from ifrs_metrics_engine.utils.choices import IFRS_STANDARD


@dataclass
class ProjectRequest:
    workspace_id : str
    name : str
    ifrs_standard : IFRS_STANDARD

class ProjectService:

    @inject
    def __init__(self ,workspace_service : WorkspaceService  = Provide["workspace_repository"]):
        self.workspace_service = workspace_service

    @atomic_op
    def create_project(self ,request : ProjectRequest):
        workspace = self.workspace_service.get_workspace(request.workspace_id)
        project = Project(workspace, request.ifrs_standard, request.name)
        if project:
            return project.save()


    def get_project(self ,project_id):
        return Project.objects.get(id=project_id)

    def get_user_projects(self):
        return Project.objects.filter()