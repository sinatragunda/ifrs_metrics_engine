# Created by Sinatra Gunda 
# Created at 24/11/2026 11:12
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from dependency_injector.wiring import inject, Provide

from ifrs_metrics_engine.apps.invitation.models import Invitation
from ifrs_metrics_engine.apps.workspace.models import WorkspaceMemberSerializer
from ifrs_metrics_engine.apps.workspace.workspace_member_service import WorkspaceMemberService


class WebhooksPostEventsService:

    @inject
    def __init__(self ,workspace_member_service : WorkspaceMemberService = Provide['workspace_member_service']):
        self.workspace_member_service = workspace_member_service


    def user_events(self ,user = None ,unsafe_metadata : dict = None):
        post_event = unsafe_metadata.get('post_event')
        match post_event:
            case 'workspace_membership_join':
                self.create_workspace_member(user ,unsafe_metadata)

    def create_workspace_member(self ,user_data ,unsafe_metadata : dict = None):
        if unsafe_metadata:
            invitation_id = unsafe_metadata.get('invitation_id')
            invitation =  Invitation.objects.get(invitation_id=invitation_id)
            workspace_member = {
                'workspace_id': invitation.workspace.id,
                'access_scope': invitation.access_scope,
                'user_id': user_data.get('id')
            }

            serializer = WorkspaceMemberSerializer(data = workspace_member)
            serializer.is_valid(raise_exception=True)
            serializer.save()
