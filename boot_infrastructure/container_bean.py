# Created by Sinatra Gunda 
# Created at 17/11/2026 07:59
# Kindly contact me at @sinatragunda or treyviis@gmail.com

from dependency_injector import containers ,providers
from dependency_injector.containers import WiringConfiguration

from ifrs_metrics_engine.apps.invitation.invitation_service import InvitationService
from ifrs_metrics_engine.apps.users.user_service import UserService
from ifrs_metrics_engine.apps.workspace.workspace_service import WorkspaceService
from ifrs_metrics_engine.utils.email.email_service import EmailService


class Container(containers.DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=['ifrs_metrics_engine.apps'])
    workspace_repository = providers.Factory(WorkspaceService)
    user_service = providers.Factory(UserService)
    email_service = providers.Factory(EmailService)
    invitation_service = providers.Factory(InvitationService ,email_service=email_service)

def wire_container():
    Container()
