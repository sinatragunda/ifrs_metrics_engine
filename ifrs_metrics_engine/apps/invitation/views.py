from dependency_injector.wiring import inject, Provide
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from boot_infrastructure.container_bean import Container
from ifrs_metrics_engine.apps.invitation.invitation_service import InvitationService, InvitationRequest
from ifrs_metrics_engine.apps.invitation.models import InvitationSerializer
from ifrs_metrics_engine.utils.context_util import get_session_user


# Create your views here.


@inject
@api_view(['POST'  ,'GET'])
def invitations(request ,invitation_service : InvitationService = Provide[Container.invitation_service]):

    method = request.method
    match method:
        case 'POST':
            send_invitation(request,invitation_service)

def send_invitation(request ,invitation_service : InvitationService = Provide[Container.invitation_service]):
        user_session = get_session_user()

        invitation_request = {
            'invites': request.data ,
            'user_id' : user_session.auth_user_id
        }

        invitation = invitation_service.send_invitation(invitation_request)
        response = InvitationSerializer(invitation ,many=False)
        return JsonResponse(response.data)