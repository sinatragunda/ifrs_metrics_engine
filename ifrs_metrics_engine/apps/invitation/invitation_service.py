# Created by Sinatra Gunda 
# Created at 19/11/2026 10:42
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import os
from dataclasses import dataclass

from dependency_injector.wiring import Provide
from django.core import signing
from django.db import transaction

from boot_infrastructure.container_bean import Container
from ifrs_metrics_engine.apps.invitation.models import Invitation, InvitationProject
from ifrs_metrics_engine.apps.project.models import Project
from ifrs_metrics_engine.apps.project.project_service import ProjectService
from ifrs_metrics_engine.utils.context_util import get_resources_folder
from ifrs_metrics_engine.utils.email.email_service import EmailService, EmailDetails


@dataclass
class InvitesRequest:
    email: str
    workspace_id: str
    user_id: str
    roleId: str
    projectIds : list[int]


@dataclass
class InvitationRequest:
    user_id: str
    invites : list[InvitesRequest]


SUBJECT = 'Invitation Request'

class InvitationService:

    def __init__(self ,email_service : EmailService = Provide[Container.email_service] ,project_service : ProjectService = Provide[Container.project_service] ):
        self.email_service = email_service
        self.project_service = project_service

    def send_invitation(self, invitation_request : InvitationRequest):

        user_id= invitation_request.user_id
        invites = invitation_request.invites

        if not invites:
            raise Exception('Invitation request must have at least one project')

        token = self.__create_token_link(invitation_request)

        for invite in invites:

            with transaction.atomic():

                invitation = {
                    'workspace_id' : invite.workspace_id,
                    'email' : invite.email,
                    'token' : token,
                }

                email_template_file = f'{get_resources_folder()}/mail/invitation.html'

                invitation = Invitation(**invitation)

                invitation.save()

                projects = set(invite.projectIds)

                if projects:
                    projects = Project.objects.filter(id_in = set(invite.projectIds))
                    invitation_projects  = list(map(lambda project: InvitationProject(invitation ,project),projects))
                    list(map(lambda invitation_project: invitation_project.save() ,invitation_projects))
                    InvitationProject.objects.bulk_create([InvitationProject(invitation = invitation ,project = project) for project in invitation_projects])



                email_details = EmailDetails(
                    email=invitation.email,
                    template=email_template_file,
                    subject=SUBJECT)

                self.email_service.send_email(email_details)

                transaction.on_commit(lambda: self.email_service.send_email(email_details))

    def approve_invitation(self, invitation):
        pass

    def decline_invitation(self, invitation):
        pass

    def revoke_invitation(self, invitation):
        pass

    def __create_token_link(self, invitation_request):

        token = signing.dumps({
            'workspace_id' : invitation_request.workspace_id,
            'sender_id' : invitation_request.user_id,
        },
        salt ="email-verify")

        print(token)

        return token