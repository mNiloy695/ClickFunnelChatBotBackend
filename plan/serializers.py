from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Plan
        fields='__all__'
        read_only_fields=['created_at','updated_at']





class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Plan
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