
from django.urls import include ,path

from ifrs_metrics_engine.api.v1.root_view import api_root
from ifrs_metrics_engine.apps.workspace.views import workspaces_route

urlpatterns = [
    path("" ,api_root ,name = "root"),
    path("workspace/" ,workspaces_route ,name ="CRUD Workspaces"),
]