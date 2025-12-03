# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Subscription
# from datetime import timedelta
# from django.utils import timezone
# from datetime import datetime
# from .models import InvoiceModel
# @receiver(post_save,sender=Subscription)
# def subscription_created(sender,instance,created,**kwargs):
#     if created:
#         duration=instance.duration
#         plan=instance.plan
#         instance.price=plan.price

#         user=instance.user

#         if user.is_subscribed:
#             user.is_subscribed=True
#             user.save()

#         if not instance.is_active:
#             instance.is_active=True
#         if duration=='weekly':
#             instance.end_date=instance.start_date + timedelta(weeks=1)
#         elif duration=='monthly':
#             instance.end_date=instance.start_date + timedelta(days=30)
#         elif duration=='yearly':
#             instance.end_date=instance.start_date + timedelta(days=365)
#         elif duration=='lifetime':
#             instance.end_date=instance.start_date + timedelta(days=datetime.max)  
#         instance.save()

#         InvoiceModel.objects.create(
#             user=user,
#             plan=plan,
#             duration=duration,
#             start_date=instance.start_date,
#             end_date=instance.end_date,
#             status="paid",
#             amount=instance.price
#         )
    