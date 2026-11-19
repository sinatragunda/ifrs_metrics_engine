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
from ifrs_metrics_engine.utils.email.email_service import EmailService, EmailDetails


@dataclass
class InvitationRequest:
    email: str
    workspace_id: str
    user_id: str
    email : str
    projects : list[int]

SUBJECT = 'Invitation Request'

class InvitationService:

    def __init__(self ,email_service : EmailService = Provide[Container.email_service] ,project_service : ProjectService = Provide[Container.project_service] ):
        self.email_service = email_service
        self.project_service = project_service

    def send_invitation(self, invitation_request : InvitationRequest):

        project_ids  = set(invitation_request.projects)

        if not project_ids:
            raise Exception('Invitation request must have at least one project')

        token = self.__create_token_link(invitation_request)

        projects = Project.objects.filter(id__in=project_ids)

        with transaction.atomic():

            invitation = {
                'workspace_id' : invitation_request.workspace_id,
                'email' : invitation_request.email,
                'token' : self.__create_token_link(invitation_request),
            }

            invitation = Invitation(**invitation)

            invitation.save()

            invitation_projects  = list(map(lambda project: InvitationProject(invitation ,project),projects))

            list(map(lambda invitation_project: invitation_project.save() ,invitation_projects))

            InvitationProject.objects.bulk_create([InvitationProject(invitation = invitation ,project = project) for project in invitation_projects])

            email_details = EmailDetails(
                email=invitation.email,
                template='/resources/mail/invitation.html',
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