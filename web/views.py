from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Internal funcions imports
from web.serializers import *

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomerRegistrationView(APIView):
    def post(self,request):
        data = request.data
        try:
            user = CustomUser.objects.create_user(
                first_name=data["first_name"], last_name=data["last_name"],
                email=data["email"], phone=data["phone"],username=data["username"]
            )
        except Exception as e:
            response = {
                "resp_code":0,
                "message":f"{e}"
            }
        else:
            data["user"] =  user.id
            serializer = CustomerCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message":"User creation completed succesfully.",
                    "resp_code":1
                }
            else:
                response = {
                    "resp_code":0,
                    "message":serializer.errors
                }
        return Response(response)
