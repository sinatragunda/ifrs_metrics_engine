from dependency_injector.wiring import inject, Provide
from django.http import JsonResponse
from rest_framework.decorators import api_view

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

def send_invitation(request ,invitation_service : InvitationService):

        user_session = get_session_user()

        invitation_request = InvitationRequest(invites = request.data,user_id = user_session.auth_user_id)

        print('invitation request data',invitation_request)

        invitation = invitation_service.send_invitation(invitation_request)

        response = InvitationSerializer(invitation ,many=False)

        return JsonResponse(response.data)