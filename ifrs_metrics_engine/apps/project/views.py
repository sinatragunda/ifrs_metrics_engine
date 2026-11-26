import json

from dependency_injector.wiring import inject, Provide
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from starlette.status import HTTP_200_OK

from api.api_utils import json_response
from ifrs_metrics_engine.apps.project import project_service
from ifrs_metrics_engine.apps.project.models import ProjectTemplateSerializer, ProjectSerializer, ProjectsRequest, \
    ProjectResponseSerializer
from ifrs_metrics_engine.apps.project.project_service import ProjectService


# Create your views here.

@api_view(['POST' ,'GET'])
@inject
def projects_view(request ,project_service : ProjectService = Provide['project_service']):
    method = request.method

    match method:
        case 'GET':
            pass
        case 'POST':
            return __create_project(request ,project_service)


@api_view(['GET'])
def projects_template(request, format = 'json'):
    serializer = ProjectTemplateSerializer(data={})
    serializer.is_valid(raise_exception=True)
    return JsonResponse(serializer.data ,status = status.HTTP_200_OK ,safe = False)


@api_view(['GET'])
@inject
def get_workspace_projects(request,workspace_id, project_service : ProjectService = Provide['project_service']):
    projects = project_service.get_workspace_projects(workspace_id)
    serializer = ProjectResponseSerializer(projects, many=True)
    return json_response(serializer ,status=HTTP_200_OK)

def __create_project(request ,project_service : ProjectService):

    project_request = ProjectsRequest(**request.data)
    project = project_service.create_project(project_request)
    serializer = ProjectSerializer(instance= project , many = False)
    return json_response(serializer ,status = status.HTTP_201_CREATED)