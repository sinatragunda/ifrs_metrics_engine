# Created by Sinatra Gunda 
# Created at 17/11/2026 10:53
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.db.models import QuerySet

class WorkspaceQuerySet(QuerySet):

    def linked_users(self):
        pass