from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.


# name , description,price,duration, created_at,updated_at 
DURATION_TYPE=(
    ('monthly','Monthly'),
    ('weekly','Weekly'),
    ('yearly','Yearly'),
    ('lifetime','Lifetime'),
)


class Plan(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    duration=models.CharField(choices=DURATION_TYPE,max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name



class Subscription(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='subscriptions')
    plan=models.ForeignKey(Plan,on_delete=models.CASCADE,related_name='subscriptions')
    duration=models.CharField(choices=DURATION_TYPE,max_length=20)
    start_date=models.DateTimeField(auto_now_add=True)
    end_date=models.DateTimeField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.email} - {self.plan.name} Subscription"