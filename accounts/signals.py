from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance,
                                   first_name=instance.first_name,
                                   last_name=instance.last_name
                                   )
        




@receiver(post_save, sender=UserProfile)
def update_user_names(sender, instance, created, **kwargs):
    user = instance.user
    changed = False

    if user.first_name != instance.first_name:
        user.first_name = instance.first_name
        changed = True

    if user.last_name != instance.last_name:
        user.last_name = instance.last_name
        changed = True

    if changed:  
        user.save()
