from django.urls import path,include
from .views import PlanView,SubscriptionView,InvoiceView,CreateCheckoutSessionView
from rest_framework.routers import DefaultRouter
from .webhook import stripe_webhook
router=DefaultRouter()
router.register('list',PlanView,basename='plans')
router.register('subscriptions/list',SubscriptionView,basename='subscriptions')

urlpatterns = [
    path('',include(router.urls)),
    path('invoices/',InvoiceView.as_view(),name="invoices"),
    path('invoices/<int:pk>/',InvoiceView.as_view(),name='invoice-details'),
    path('stripe-check-out/',CreateCheckoutSessionView.as_view(),name="stripe-checkout"),
    path('webhook/',stripe_webhook)
]
