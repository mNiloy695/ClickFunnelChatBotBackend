from django.urls import path,include
from .views import PlanView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('plans',PlanView,basename='plans')
urlpatterns = [
    path('',include(router.urls)),
]
