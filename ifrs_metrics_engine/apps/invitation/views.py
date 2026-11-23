from dependency_injector.wiring import inject, Provide
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.api_utils import json_response
from ifrs_metrics_engine.apps.invitation.invitation_service import InvitationService, InvitationRequest
from ifrs_metrics_engine.apps.invitation.models import InvitationSerializer
from ifrs_metrics_engine.apps.workspace.models import WorkspaceMemberSerializer
from ifrs_metrics_engine.utils.context_util import get_session_user


# Create your views here.


@api_view(['POST'  ,'GET'])
@inject
def invitations(request ,invitation_service : InvitationService = Provide['invitation_service']):

    method = request.method
    match method:
        case 'POST':
            return send_invitation(request,invitation_service)
        case 'GET':
            return get_invitations(invitation_service)


@api_view(['POST'])
@inject
def confirm_invitation(request ,invitation_service : InvitationService = Provide['invitation_service']):

    token = request.data.get('token')

    print(request.data)

    workspace_member = invitation_service.approve_invitation(token)

    print("workspace_member",workspace_member)
    serializer = WorkspaceMemberSerializer(workspace_member)

    return json_response(serializer, status=status.HTTP_201_CREATED)


def get_invitations(invitation_service : InvitationService):
    user_id = get_session_user().auth_user_id
    invitations = invitation_service.get_invitations(user_id)
    seralizer = InvitationSerializer(invitations , many=True)
    return JsonResponse(seralizer.data, status=status.HTTP_200_OK)

def send_invitation(request ,invitation_service : InvitationService):

    user_session = get_session_user()

    invitation_request = InvitationRequest(invites = request.data,user_id = user_session.auth_user_id)

    print('invitation request data',invitation_request)

    invitations = invitation_service.send_invitation(invitation_request)

    print('invitation data after creation',invitations.__str__() ,' and type ' ,type(invitations))

    return Response(status=status.HTTP_201_CREATED)

