from django.db import models

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
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    duration=models.CharField(choices=DURATION_TYPE,max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


