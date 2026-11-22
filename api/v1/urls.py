
from django.urls import include ,path

from api.v1.root_view import api_root
from ifrs_metrics_engine.apps.invitation.views import invitations, confirm_invitation
from ifrs_metrics_engine.apps.workspace.views import workspaces_route

urlpatterns = [
    path("" ,api_root ,name = "root"),
    path("workspace/" ,workspaces_route ,name ="CRUD Workspaces"),
    path("invitation/" ,invitations ,name ="CRUD Invitations"),
    path("confirm_invitation" ,confirm_invitation ,name ="Confirm Invitations"),
]