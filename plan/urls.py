from django.urls import path,include
from .views import PlanView,SubscriptionView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('list',PlanView,basename='plans')
router.register('subscriptions/list',SubscriptionView,basename='subscriptions')
urlpatterns = [
    path('',include(router.urls)),
]
