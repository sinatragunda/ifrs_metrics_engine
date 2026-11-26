# Created by Sinatra Gunda 
# Created at 25/11/2026 01:38
# Kindly contact me at @sinatragunda or treyviis@gmail.com
from django.http import JsonResponse
from boot_infrastructure.exceptions.custom_exceptions import NotAuthenticatedWithLoginRequirement

class ExceptionsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, NotAuthenticatedWithLoginRequirement):
            return JsonResponse({
                'status': 401,
                'errors': exception.default_code,
                'message': str(exception),
                'requireLogin': exception.require_login
            }, status=401)

        return None