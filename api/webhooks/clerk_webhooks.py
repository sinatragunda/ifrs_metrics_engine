# Created by Sinatra Gunda 
# Created at 24/11/2026 08:29
# Kindly contact me at @sinatragunda or treyviis@gmail.com
import json
import os

from dependency_injector.wiring import inject, Provide
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from standardwebhooks import WebhookVerificationError
from svix import Webhook

from boot_infrastructure.container_bean import Container

WEBHOOK_SECRET = os.environ.get('CLERK_SIGNING_SECRET')

@csrf_exempt
@api_view(['POST'])
def webhooks_handler(request):
    try:
        print("webhook user creation event")
        from ifrs_metrics_engine.apps.users.user_service import UserService

        user_service : UserService= Container.user_service()

        webhook = Webhook(WEBHOOK_SECRET)

        body  = request.body

        webhook.verify(body,request.headers)
        event = json.loads(body)

        event_type = event['type']
        data = event['data']

        print(body)

        if event_type == 'user.created':
            user_service.create_user_webhook(data)
            return JsonResponse({'status': 'success'} ,status=200)
    except WebhookVerificationError as e:
        e.with_traceback()
        raise e
    except Exception as e:
        print(e)
        raise e
