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
    stripe_product_price_id=models.CharField(max_length=1000,null=True,blank=True)
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
    end_date=models.DateTimeField(null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0,blank=True)
    is_active=models.BooleanField(default=True,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.email} - {self.plan.name} Subscription"
    


STATUS=(
    ('paid','paid'),
    ('unpaid','unpaid')
)

class InvoiceModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='invoices')
    plan=models.ForeignKey(Plan,on_delete=models.SET_NULL,related_name="plan_invoices",null=True)
    invoice_id=models.CharField(unique=True,null=True,blank=True)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    duration=models.CharField(choices=DURATION_TYPE,max_length=10)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(choices=STATUS,max_length=10,default="paid")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    