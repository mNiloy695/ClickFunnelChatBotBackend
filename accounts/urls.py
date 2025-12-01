from django.urls import path,include
from .views import RegistrationView,LoginView,UserProfileView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('profile',UserProfileView,basename='profile')

urlpatterns = [
    path('register/',RegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('',include(router.urls)),
]
