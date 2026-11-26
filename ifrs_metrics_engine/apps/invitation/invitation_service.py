# Created by Sinatra Gunda 
# Created at 19/11/2026 10:42
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import datetime
import hmac
import os
import time
import uuid
from dataclasses import dataclass, asdict

from dependency_injector.wiring import Provide, inject
from django.core import signing
from django.core.signing import SignatureExpired
from django.db import transaction, IntegrityError

from boot_infrastructure.exceptions.custom_exceptions import BadRequestException, TokenExpiredException
from ifrs_metrics_engine.apps import workspace
from ifrs_metrics_engine.apps.invitation.models import Invitation, InvitationProject, InvitationSerializer
from ifrs_metrics_engine.apps.project.models import Project
from ifrs_metrics_engine.apps.project.project_service import ProjectService
from ifrs_metrics_engine.apps.users.user_service import UserService
from ifrs_metrics_engine.apps.workspace.models import Workspace, WorkspaceSerializer, WorkspaceMemberSerializer
from ifrs_metrics_engine.utils.annotations import atomic_op
from ifrs_metrics_engine.utils.choices import INVITATION_STATUS, ACCESS_SCOPES
from ifrs_metrics_engine.utils.context_util import get_session_user
from ifrs_metrics_engine.utils.email.email_service import EmailService, EmailDetails


@dataclass
class InvitesRequest:
    email: str
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
    def __init__(self ,email_service : EmailService = Provide["email_service"] ,project_service : ProjectService = Provide['project_service'] ,user_service: UserService = Provide["user_service"] ):
        self.email_service = email_service
        self.project_service = project_service
        self.user_service = user_service

    def get_invitations(self,user_id):
        return Invitation.objects.filter(invited_by = user_id)

    def send_invitation(self, invitation_request : InvitationRequest):

        user_id= invitation_request.user_id
        invites: list[InvitesRequest] = invitation_request.invites
        user_session = get_session_user()
        invited_by = user_session.user_model
        invitations = []

        if not invites:
            raise Exception('Invitation request must have at least one project')

        with transaction.atomic():

            for raw_invite in invites:

                print('invite data','of type ',type(raw_invite), raw_invite)

                invite = InvitesRequest(**raw_invite)

                invite_id = f'invite-{uuid.uuid4().hex}'

                is_workspace_invite = self.__is_workspace_invitation(invite)

                workspace = Workspace.objects.get(workspace_id = invite.workspaceId)

                expires_at  = self.__token_expiration_time()
                token = self.__create_token(invite, user_id,invite_id,is_workspace_invite)

                print('Creating user with invite id ',invite_id)

                invitation = {
                    'workspace' : workspace.id,
                    'email' : invite.email,
                    'token' : token,
                    'status' : INVITATION_STATUS.PENDING,
                    'invited_by': invited_by.id,
                    'access_scope': ACCESS_SCOPES(invite.roleId),
                    'expires_at': expires_at
                }

                email_template_file = 'mail/invitation.html'

                serializer = InvitationSerializer(data = invitation)
                serializer.is_valid(raise_exception=True)

                print(invited_by)

                try:
                    invitation = serializer.save(created_by = invited_by, invitation_id = invite_id)
                except IntegrityError as e:
                    print('current details',e)
                    raise e

                # check if its a project invite or a project membership

                mail_content = {
                    'token': token,
                    'invited_by': user_session.username,
                    'workspace_name' : workspace.name,
                    'expires_at': expires_at,
                }

                print("invite request is ",invitation)

                if not is_workspace_invite:
                    projectIds = set(invite.projectIds)
                    projects = Project.objects.filter(id_in = projectIds)
                    invitation_projects  = list(map(lambda project: InvitationProject(invitation ,project),projects))
                    InvitationProject.objects.bulk_create([InvitationProject(invitation = invitation ,project = project) for project in invitation_projects])
                    mail_content['confirm_url'] = self.__create_token_link(token)
                else:
                    mail_content['confirm_url'] = self.__create_token_link(token)

                email_details = EmailDetails(
                    to=[invitation.email],
                    template=email_template_file,
                    body='',
                    context=mail_content,
                    subject=SUBJECT)

                print("mail details", email_details)

                transaction.on_commit(lambda: self.email_service.send_email(email_details))

                invitations.append(invitation)

        return invitations

    @atomic_op
    def approve_invitation(self, token):

        decoded_token = self.__decode_token(token)

        invitation_id = decoded_token['invite_id']

        invitation  = Invitation.objects.get(invitation_id = invitation_id)

        if (
            not invitation
            or not hmac.compare_digest(str(invitation.token), str(token))
            #or invitation.status != INVITATION_STATUS.PENDING
        ):
            raise BadRequestException('Failed to validate invitation.Token or invitation details invalid')


        #invitation.status = INVITATION_STATUS.ACCEPTED
        invitation.accepted_at = datetime.datetime.now()

        invitation.save()

        user = self.user_service.clerk_create_user(invitation.email)
        workspace = invitation.workspace

        workspace_member_serializer = WorkspaceMemberSerializer(data = {
            #'user' : user.id,
            'workspace' : workspace.id,
            'access_scope':invitation.access_scope,
        },context={'email': invitation.email})

        print('worspace serializer ' ,workspace_member_serializer.context)

        workspace_member_serializer.is_valid(raise_exception=True)

        workspace_member_serializer.save()

        # create user record now if it doesn't exists yet
        # proceed in creating membership to project
        return workspace_member_serializer


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

    def __create_token_link(self ,token):
        return f'{BASE_FRONT_END_URL}/confirm_invitation?token={token}'


    def __decode_token(self ,token):

        max_age = int(float(os.environ['CONFIRMATION_EXPIRE_TIME_IN_MINUTES'])) * 60
        print("max token age",max_age)
        try:
            return signing.loads(token ,max_age= max_age ,salt="email-verify")
        except SignatureExpired:
            raise TokenExpiredException('Failed to authenticate or validate invitation. Signature expired')
        except Exception as e:
            print(e)
            raise e


    def __create_token(self, invite_request : InvitesRequest ,user_id,invite_id, is_workspace_invite = False):

        print(invite_request)

        token_encoded_data = {
            'workspace_id': invite_request.workspaceId,
            'sender_id': user_id,
            'email': invite_request.email,
            'invite_id': invite_id,
        }

        if is_workspace_invite:
            token = signing.dumps(token_encoded_data,salt="email-verify")
        else:
            token_encoded_data = {
                **token_encoded_data,
                'project_ids': invite_request.projectIds,
            }
            token = signing.dumps(token_encoded_data,salt = "email-verify")

        print(token)

        return token