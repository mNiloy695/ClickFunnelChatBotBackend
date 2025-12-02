from django.shortcuts import render
from .serializers import RegistrationSerializer,LoginSerializer,UserProfileSerializer,LogoutSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


class RegistrationView(APIView):
    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User registered successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            refresh_token=RefreshToken.for_user(user)

            return Response({"message":"Login successful",
                            "user":
                            {
                            'id':user.id,
                            "email":user.email,
                            'username':user.username,
                            "first_name":user.first_name,
                            "last_name":user.last_name,
                            "is_subscribed":user.is_subscribed,
                            "date_joined":user.date_joined,
                            'refresh':str(refresh_token),
                            'access':str(refresh_token.access_token),
                            }
                            },
                            status=status.HTTP_200_OK
                            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

from .models import UserProfile
class UserProfileView(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=UserProfileSerializer
    def get_queryset(self):
        return UserProfile.objects.select_related('user').filter(user=self.request.user)
    


class LogoutView(APIView):
    def post(self,request):
        serializer=LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token=serializer.validated_data['refresh']
            try:
                token=RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message":"Logout successful"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)