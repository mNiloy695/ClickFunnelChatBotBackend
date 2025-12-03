from  django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Subscription,Plan
import stripe
from .models import Plan,Subscription
from django.contrib.auth import get_user_model
User=get_user_model()
@csrf_exempt

def stripe_webhook(request):
    payload=request.body
    sig_header=request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret='your_endpoint_secret'

    try:
        event=stripe.Webhook.construct_event(
            payload,sig_header,endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'status':'invalid payload'},status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'status':'invalid signature'},status=400)
    if event['type']=='checkout.session.completed':
        session=event['data']['object']
        metadata=session.get('metadata',{})
        user_id=metadata.get('user_id')
        plan_id=metadata.get('plan_id')
        duration=metadata.get('duration')
        plan=Plan.objects.get(id=plan_id)
        user=User.objects.get(id=user_id)

        subscription,created=Subscription.objects.get_or_create(
            user=user,
            plan=plan,
            defaults={
               "duration":duration
            }
        )

     



        


        
