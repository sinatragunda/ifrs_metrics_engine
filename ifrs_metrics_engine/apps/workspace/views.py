from dependency_injector.wiring import Provide, inject
from django.http import JsonResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from boot_infrastructure.container_bean import Container
from boot_infrastructure.context.user_session_context import user_session_context_var
from ifrs_metrics_engine.apps.workspace.models import Workspace, WorkspaceSerializer
from ifrs_metrics_engine.apps.workspace.workspace_repository import WorkspaceRepository
from ifrs_metrics_engine.utils.context_util import get_session_user


# Create your views here.

@api_view(['GET' ,'POST','DELETE'])
@inject
def workspaces_route(request ,workspace_repository : WorkspaceRepository=Provide[Container.workspace_repository]):
    request_method = request.method
    if request_method == 'GET':
        return get_user_workspaces(request ,workspace_repository)
    elif request_method == 'POST':
        return create_user_workspaces(request,workspace_repository)


def get_user_workspaces(request,workspace_repository : WorkspaceRepository):
    print("get_user_workspaces ,check id from token directly")
    user_data  = get_user_data()
    workspaces = workspace_repository.get_workspace_by_user_id(user_data.auth_user_id)
    response = WorkspaceSerializer(workspaces, many=True)
    return JsonResponse(response.data ,safe=False)

def create_user_workspaces(request ,workspace_repository : WorkspaceRepository):

    user_data = get_session_user()
    user_model = user_data.user_model

    payload = request.data

    print(type(payload), payload)

    kwargs = {
        'name': payload['name'],
        'workspace_id': payload['id'],
        'user_id' : user_data.auth_user_id,
        'created_by' : user_model
    }

    workspace = Workspace(**kwargs)

    print(f"create_user_workspaces ,check id from token directly {workspace}")

    workspace = workspace_repository.save(workspace)
    response = WorkspaceSerializer(workspace, many=True)

    return JsonResponse(response.data,safe=False,status=HTTP_201_CREATED)

def get_user_data():
    user_data = user_session_context_var.get()
    if not user_data:
        raise HTTP_400_BAD_REQUEST

    return user_data