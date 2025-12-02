from django.shortcuts import render
from .serializers import PlanSerializer
from .models import Plan
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
# Create your views here.

  
class PlanView(ModelViewSet):
    queryset=Plan.objects.all()
    serializer_class=PlanSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
