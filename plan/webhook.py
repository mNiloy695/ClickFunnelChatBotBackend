from  django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Subscription,Plan
import stripe
from .models import Plan,Subscription
from django.contrib.auth import get_user_model
from datetime import timezone,timedelta,datetime
from django.conf import settings
User=get_user_model()


webhook_secrect=settings.STRIPE_WEBHOOK_KEY
@csrf_exempt
def stripe_webhook(request):
    payload=request.body
    sig_header=request.META.get('HTTP_STRIPE_SIGNATURE')


    try:
        event=stripe.Webhook.construct_event(
            payload,sig_header,webhook_secrect

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
        # duration=metadata.get('duration')
        plan=Plan.objects.get(id=plan_id)
        user=User.objects.get(id=user_id)
        duration=plan.duration
        paymet_id=session.get("payment_intent")
        subscription,created=Subscription.objects.get_or_create(
            user=user,
            plan=plan,
            defaults={
               "duration":duration,
               "price":plan.price,
               "is_active":True
               

            }
        )

        if subscription:
            now=timezone.now()
            subscription.start_date=now
            
            if duration=="lifetime":
                subscription.end_date= now+timedelta(days=datetime.max)
            if duration=="yearly":
                subscription.end_date=now+timedelta(days=365)
            if duration=="monthly":
                subscription.duration=now+timedelta(days=30)
            if duration=="weekly":
                subscription.end_date=now()+timedelta(days=7)
            
            subscription.is_active=True


            subscription.save()
        
        user.is_subscribed=True
        user.save()

        from .models import InvoiceModel
        if created or subscription:
            subs=created if created else subscription

            #"invoice_id","start_date","end_date","duration","amount","status"
            InvoiceModel.objects.create(
                invoice_id=f"INV_{paymet_id}",
                user=user,
                plan=plan,
                amount=plan.price,
                start_date=subs.start_date,
                end_date=subs.end_date,
                duration=subs.duration,
                status="paid"

            )
        
        return JsonResponse({'status': 'success'})

            



        


        
