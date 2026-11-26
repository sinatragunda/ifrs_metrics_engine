# Created by Sinatra Gunda 
# Created at 19/11/2026 09:36
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import json

from dependency_injector.wiring import inject, Provide
from django.forms import model_to_dict
from rest_framework.exceptions import NotFound

from boot_infrastructure.context.user_session_context import UserSession
from ifrs_metrics_engine.apps.project.models import Project, ProjectsRequest, ProjectSerializer
from ifrs_metrics_engine.apps.users.user_service import UserService
from ifrs_metrics_engine.apps.workspace import workspace_service
from ifrs_metrics_engine.apps.workspace.models import Workspace
from ifrs_metrics_engine.apps.workspace.workspace_service import WorkspaceService
from ifrs_metrics_engine.utils.annotations import atomic_op
from ifrs_metrics_engine.utils.choices import IFRS_STANDARD, ACCESS_SCOPES
from ifrs_metrics_engine.utils.context_util import get_session_user


class ProjectService:

    @inject
    def __init__(self ,workspace_service : WorkspaceService  = Provide["workspace_repository"]):
        self.workspace_service = workspace_service

    @atomic_op
    def create_project(self ,project_request : ProjectsRequest)-> Project:

        user_session : UserSession = get_session_user()
        user_id = user_session.auth_user_id

        ifrs_standard = IFRS_STANDARD(project_request.standard)

        print(ifrs_standard,user_id)

        workspace_id = project_request.workspaceId
        workspace_filter = {'workspace_id':workspace_id}
        if str(workspace_id) == 'main':
            workspace_filter['name'] = 'main'
            del workspace_filter['workspace_id']

        workspace = self.workspace_service.get_workspace_by_filter_key(**workspace_filter)

        if not workspace:
            if not str(workspace_id).__eq__('main'):
                raise NotFound(f"Workspace with id {workspace_id} does not exist")
            # create main workspace
            main_workspace = Workspace(name = workspace_id,user_id= user_id ,created_by = user_session.user_model)
            workspace = self.workspace_service.create(main_workspace)

        print("workspace data ",json.dumps(model_to_dict(workspace),indent=4))

        data = {
            'ifrs_standard': ifrs_standard,
            'name' : project_request.name,
            'workspace' : workspace.id
        }

        print("user id is ",model_to_dict(user_session.user_model))

        serializer = ProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(created_by = user_session.user_model)

        return project

    def get_project(self ,project_id):
        return Project.objects.get(id=project_id)

    def get_user_projects(self):
        return Project.objects.filter()


    def get_workspace_projects(self, workspace_id):
        return Project.objects.filter(workspace_id=workspace_id)