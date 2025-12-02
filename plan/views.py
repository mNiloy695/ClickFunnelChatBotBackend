from django.shortcuts import render
from .serializers import PlanSerializer,SubscriptionSerializer
from .models import Plan,Subscription
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

  
class PlanView(ModelViewSet):
    queryset=Plan.objects.all()
    serializer_class=PlanSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SubscriptionView(ModelViewSet):
    queryset=Subscription.objects.select_related('user','plan').all()
    serializer_class=PlanSerializer
    permission_classes=[permissions.IsAuthenticated]
     

