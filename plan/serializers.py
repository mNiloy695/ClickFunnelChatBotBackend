from rest_framework import serializers
from .models import Plan,Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Plan
        fields='__all__'
        read_only_fields=['created_at','updated_at']
    def validate(self, attrs):
        stripe_product_price_id=attrs.get('stripe_product_price_id')
        if not stripe_product_price_id:
            raise serializers.ValidationError({"error":"stripe_product_price_id is required"})
        return attrs

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subscription
        fields='__all__'
        read_only_fields=['created_at','updated_at','price','is_active']
    
    def validate(self, attrs):
        user=attrs.get('user',None)
        plan=attrs.get('plan',None)
        duration=attrs.get('duration',None) 

        if not user:
            raise serializers.ValidationError({"error":"User is required"})
        if not plan:
            raise serializers.ValidationError({"error":"Plan is required"})
        if not duration:
            raise serializers.ValidationError({"error":"Duration is required"})

        return attrs

from .models import InvoiceModel
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=InvoiceModel
        fields="__all__"
        read_only_fields=["created_at","updated_at","invoice_id"]