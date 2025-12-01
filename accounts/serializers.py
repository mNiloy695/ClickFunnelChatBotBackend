from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    
    class Meta:
        model=CustomUser
        fields=['username','email','first_name','last_name','password','confirm_password','is_subscribed']
        read_only_fields=['is_staff','is_active','date_joined','is_subscribed']
    
    def validate(self, attrs):
        email=attrs.get('email',None)
        password=attrs.get('password',None)
        confirm_password=attrs.pop('confirm_password',None)
        username=attrs.get('username',None)

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error":"Username is already exist"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error":"Email is already exist"})
        if not password or not confirm_password:
            raise serializers.ValidationError({"error":"Password and Confirm Password is required"})

        if password != confirm_password:
            raise serializers.ValidationError({"error":"Password and Confirm Password doesn't match"})
        return attrs
    
    def create(self, validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        email=attrs.get('email',None)
        password=attrs.get('password',None)

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error":"Invalid email"})
        user=User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError({"error":"Invalid Password"})
        attrs['user']=user
        return attrs