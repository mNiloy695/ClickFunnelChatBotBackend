from django.shortcuts import render
from .serializers import RegistrationSerializer,LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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

            return Response({"message":"Login successful",
                            "user":
                            {"email":user.email,
                            "first_name":user.first_name,
                            "last_name":user.last_name}},
                            status=status.HTTP_200_OK
                            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)