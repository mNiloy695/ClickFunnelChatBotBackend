from django.urls import path,include
from .views import PlanView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('list',PlanView,basename='plans')
urlpatterns = [
    path('',include(router.urls)),
]
