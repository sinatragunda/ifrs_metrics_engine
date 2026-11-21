# Created by Sinatra Gunda 
# Created at 19/11/2026 10:42
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import datetime
import os
from dataclasses import dataclass

from dependency_injector.wiring import Provide, inject
from django.core import signing
from django.db import transaction

from ifrs_metrics_engine.apps.invitation.models import Invitation, InvitationProject
from ifrs_metrics_engine.apps.project.models import Project
from ifrs_metrics_engine.apps.project.project_service import ProjectService
from ifrs_metrics_engine.apps.workspace.models import Workspace, WorkspaceMember
from ifrs_metrics_engine.utils.choices import INVITATION_STATUS
from ifrs_metrics_engine.utils.context_util import get_resources_folder, get_session_user
from ifrs_metrics_engine.utils.email.email_service import EmailService, EmailDetails


@dataclass
class InvitesRequest:
    email: str
    inviteId: str
    workspaceId: str
    roleId: str
    roleName: str
    projectIds : list[int]


@dataclass
class InvitationRequest:
    user_id: str
    invites : list[InvitesRequest]


SUBJECT = 'Invitation Request'
BASE_FRONT_END_URL = os.environ.get('BASE_FRONT_END_URL')

class InvitationService:

    @inject
    def __init__(self ,email_service : EmailService = Provide["email_service"] ,project_service : ProjectService = Provide['project_service'] ):
        self.email_service = email_service
        self.project_service = project_service

    def send_invitation(self, invitation_request : InvitationRequest):

        user_id= invitation_request.user_id
        invites = invitation_request.invites
        user_session = get_session_user()

        if not invites:
            raise Exception('Invitation request must have at least one project')

        for invite in invites:

            with transaction.atomic():

                print('invite data','of type ',type(invite), invite)
                invite = InvitesRequest(**invite ,)
                is_workspace_invite = self.__is_workspace_invitation(invite)
                workspace = Workspace.objects.get(workspace_id = invite.workspaceId)
                token = self.__create_token(invite,user_id , self.__is_workspace_invitation(invite))


                print('loggeed user model', user_session.user_model)

                invitation = {
                    'workspace' : workspace,
                    'email' : invite.email,
                    'token' : token,
                    'status' : INVITATION_STATUS.PENDING,
                    'invited_by': user_session.user_model,
                    'expires_at': self.__token_expiration_time()
                }

                email_template_file = 'mail/invitation.html'

                invitation = Invitation(**invitation)

                invitation.save()

                # check if its a project invite or a project membership

                mail_content = {
                    'token': token,
                    'invited_by': user_session.username,
                    'workspace_name' : workspace.name,
                }

                print("invite response is ",invite)

                if not is_workspace_invite:
                    projectIds = set(invite.projectIds)
                    projects = Project.objects.filter(id_in = projectIds)
                    invitation_projects  = list(map(lambda project: InvitationProject(invitation ,project),projects))
                    InvitationProject.objects.bulk_create([InvitationProject(invitation = invitation ,project = project) for project in invitation_projects])
                    mail_content['confirm_url'] = self.__create_token_link(token ,invite.inviteId)
                else:
                    workspace = Workspace.objects.get(workspace_id = invite.workspaceId)
                    workspace_member = WorkspaceMember(workspace = workspace,access_scope =  invite.roleId)
                    workspace_member.save()
                    mail_content['confirm_url'] = self.__create_token_link(token ,invite.inviteId)

                email_details = EmailDetails(
                    to=[invitation.email],
                    template=email_template_file,
                    body='',
                    context=mail_content,
                    subject=SUBJECT)

                print("mail details", email_details)

                self.email_service.send_email(email_details)

                transaction.on_commit(lambda: self.email_service.send_email(email_details))

    def approve_invitation(self, invitation):
        pass

    def decline_invitation(self, invitation):
        pass

    def revoke_invitation(self, invitation):
        pass


    def __token_expiration_time(self):
        token_expiration = float(os.environ.get('confirmation_expire_time_in_minutes'))
        return datetime.datetime.now() + datetime.timedelta(minutes=token_expiration)


    # check if its an inviite for sending a workspace or project
    def __is_workspace_invitation(self ,inviteRequest : InvitesRequest):
        if inviteRequest.workspaceId:
            return True
        return False

    def __create_token_link(self ,token ,invite_id):
        return f'{BASE_FRONT_END_URL}/confirm_invitation?token={token}&id={invite_id}'


    def __create_token(self, invite_request : InvitesRequest ,user_id,is_workspace_invite = False):

        print(invite_request)

        if is_workspace_invite:
            token = signing.dumps({
                'workspace_id': invite_request.workspaceId,
                'sender_id': user_id,
            } ,salt="email-verify")
        else:
            token = signing.dumps({
                'project_id': invite_request.projectIds,
                'sender_id': user_id,
            } ,salt = "email-verify")


        print(token)

        return token