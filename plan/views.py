from django.shortcuts import render
from .serializers import PlanSerializer,SubscriptionSerializer,InvoiceSerializer
from .models import Plan,Subscription
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe
from rest_framework.exceptions import PermissionDenied

# Create your views here.

  
class PlanView(ModelViewSet):
    queryset=Plan.objects.all()
    serializer_class=PlanSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]




class SubscriptionView(ModelViewSet):
    queryset=Subscription.objects.select_related('user','plan')
    serializer_class=PlanSerializer
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        if self.request.method in ['POST']:
            return 
        return [permissions.IsAdminUser()]
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)



     
class CreateCheckoutSessionView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            plan_id=data.get('plan')
            user=request.user

            try: 
               plan=Plan.objects.get(id=plan_id)
            except Exception as e:
                 return Response({"error:":"Plan Model not found"}) 
            # subscription=None
            
            subscription=Subscription.objects.prefetch_related('user').filter(user=user,is_active=True).first()

            if subscription:
                previous_duration=subscription.duration
                new_duration=plan.duration

                if previous_duration==new_duration:
                    return Response({"error":"You already have this subscription kindly Upgrade"})
                
                if previous_duration=="lifetime" and new_duration=="yearly":
                    return Response({"error":"you already have life time access"})
                
                if previous_duration=="yearly" and new_duration=="monthly":
                    return Response({"error":"Wait for recent subscription expiration then you can downgrade"})
                
                if previous_duration=="monthly" and new_duration=="weekly":
                    return Response({"error":"Wait for recent subscription expiration then you can downgrade"})



            if not plan.stripe_product_price_id:
                return Response({"error": "Price ID is required the plan not have price id"}, status=status.HTTP_400_BAD_REQUEST)
            price_id=plan.stripe_product_price_id
            # print(price_id)
            
            session = stripe.checkout.Session.create(
                payment_method_types=["card",],
                
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                mode="payment",
                metadata={
        "user_id": str(user.id),
        "plan_id":str(plan_id),
        # "subscription_id": subscription.id if subscription else None 
    },
                success_url="http://127.0.0.1:8081/api/v1/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://127.0.0.1:8081/api/v1/cancel",
            )

            return Response({"checkout_url": session.url})

        except Exception as e:
            return Response({"error ms": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from .models import InvoiceModel
class InvoiceView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        data=InvoiceModel.objects.select_related("user","plan")
        user=self.request.user
        if not user.is_staff:
            data=data.filter(user=user)
        serializer=InvoiceSerializer(data,many=True)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        user=request.user

        if not user.is_staff:
            return PermissionDenied("Only Admin have permission",status=status.HTTP_403_FORBIDDEN)
    
        invoice_id=kwargs.get("pk")

        try:
            invoices=InvoiceModel.objects.select_related("user","plan").get(id=invoice_id)
        except Exception:
            return  Response({"detail": "Invoice not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=InvoiceSerializer(invoices,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors)
    



