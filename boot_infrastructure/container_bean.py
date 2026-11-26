# Created by Sinatra Gunda 
# Created at 17/11/2026 07:59
# Kindly contact me at @sinatragunda or treyviis@gmail.com

from dependency_injector import containers ,providers
from dependency_injector.containers import WiringConfiguration


class Container(containers.DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=['ifrs_metrics_engine.apps'],
                                        modules=['boot_infrastructure.middleware.clerk_authentication_middleware'],)
    workspace_repository = providers.Factory("ifrs_metrics_engine.apps.workspace.workspace_service.WorkspaceService")
    email_service = providers.Factory("ifrs_metrics_engine.utils.email.email_service.EmailService")
    project_service = providers.Factory("ifrs_metrics_engine.apps.project.project_service.ProjectService")
    workspace_member_service = providers.Factory("ifrs_metrics_engine.apps.workspace.workspace_member_service.WorkspaceMemberService")

    webhooks_post_events_service = providers.Factory("api.webhooks.post_events_service.WebhooksPostEventsService",
                                                     workspace_member_service=workspace_member_service)

    user_service = providers.Factory("ifrs_metrics_engine.apps.users.user_service.UserService" ,
                                     webhooks_post_events_service=webhooks_post_events_service)

    invitation_service = providers.Factory(
        "ifrs_metrics_engine.apps.invitation.invitation_service.InvitationService",
        email_service=email_service,
        project_service=project_service,
    )

def wire_container():
    Container()
