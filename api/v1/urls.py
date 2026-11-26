
from django.urls import include ,path

from api.v1.root_view import api_root
from api.webhooks.clerk_webhooks import webhooks_handler
from ifrs_metrics_engine.apps.invitation.views import invitations, confirm_invitation
from ifrs_metrics_engine.apps.project.views import projects_template, projects_view, get_workspace_projects
from ifrs_metrics_engine.apps.users.views import user_root_view
from ifrs_metrics_engine.apps.workspace.views import workspaces_route, get_workspace_members

urlpatterns = [
    path("" ,api_root ,name = "root"),
    path("users/" ,user_root_view ,name ="CRUD Users"),
    path("workspace/" ,workspaces_route ,name ="CRUD Workspaces"),
    path("workspace/<str:workspace_id>/members" ,get_workspace_members ,name ="Get Workspace Members"),
    path("workspace/<str:workspace_id>/projects" ,get_workspace_projects ,name ="Get Workspace Projects"),
    path("invitation/" ,invitations ,name ="CRUD Invitations"),
    path("confirm_invitation" ,confirm_invitation ,name ="Confirm Invitations"),
    path("webhooks" ,webhooks_handler ,name = "Webhooks Handler Mainly From Clerk"),
    path("projects" ,projects_view ,name = "Projects Root View"),
    path("projects/template" ,projects_template  ,name="Get Projects Template")
]