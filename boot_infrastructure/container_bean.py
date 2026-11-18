# Created by Sinatra Gunda 
# Created at 17/11/2026 07:59
# Kindly contact me at @sinatragunda or treyviis@gmail.com

from dependency_injector import containers ,providers
from dependency_injector.containers import WiringConfiguration

from ifrs_metrics_engine.apps.users.user_service import UserService
from ifrs_metrics_engine.apps.workspace.workspace_repository import WorkspaceRepository

class Container(containers.DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=['ifrs_metrics_engine.apps'])
    workspace_repository = providers.Factory(WorkspaceRepository)
    user_service = providers.Factory(UserService)

def wire_container():
    print("in init_container")
    Container()
