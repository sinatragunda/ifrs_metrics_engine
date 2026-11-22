from dependency_injector.wiring import inject, Provide
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.api_utils import json_response
from ifrs_metrics_engine.apps.invitation.invitation_service import InvitationService, InvitationRequest
from ifrs_metrics_engine.apps.invitation.models import InvitationSerializer
from ifrs_metrics_engine.utils.context_util import get_session_user


# Create your views here.


@api_view(['POST'  ,'GET'])
@inject
def invitations(request ,invitation_service : InvitationService = Provide['invitation_service']):

    method = request.method
    match method:
        case 'POST':
            send_invitation(request,invitation_service)


@api_view(['POST'])
@inject
def confirm_invitation(request ,invitation_service : InvitationService = Provide['invitation_service']):
    token = request.GET.get('token')
    invite_id = request.GET.get('id')

    invitation = invitation_service.approve_invitation(token ,invite_id)

    return json_response(invitation, status=status.HTTP_201_CREATED)


def send_invitation(request ,invitation_service : InvitationService):

        user_session = get_session_user()

        invitation_request = InvitationRequest(invites = request.data,user_id = user_session.auth_user_id)

        print('invitation request data',invitation_request)

        invitation = invitation_service.send_invitation(invitation_request)

        if invitation:

            print('invitation data after creation',invitation)
            serializer = InvitationSerializer(invitation)
            print("serialiazed respoinse" ,serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("has invitation been created ")

        return Response(
            {"detail": "Invitation could not be created or already exists."},
            status=status.HTTP_200_OK,  # or HTTP_204_NO_CONTENT / HTTP_400_BAD_REQUEST
        )