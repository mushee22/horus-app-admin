from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Internal funcions imports
from web.serializers import *
from baseapp.mixins import LoginRequiredMixin

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomerRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = request.data.copy()
            data['user'] = user.id
            customer_serializer = CustomerCreateSerializer(data=data)
            if customer_serializer.is_valid():
                customer_serializer.save()
                return Response({
                    "message": "User creation completed successfully.",
                    "resp_code": 1
                })
            else:
                return Response({
                    "resp_code": 0,
                    "message": customer_serializer.errors
                })
        else:
            return Response({
                "resp_code": 0,
                "message": serializer.errors
            })
    
    
class CustomerProfileView(LoginRequiredMixin,APIView):
    def get(self,request):
        try:
            student = Student.objects.get(user=request.user)
        except:
            response = {"resp_code":0,"message":"Student not found","data":{}}
        else:
            serializer = PersonalProfileSerilizer(student)
            response = {"resp_code":1,"message":"success","data":serializer.data}
        return Response(response)
    
    
class ProfileUpdateView(LoginRequiredMixin,APIView):
    def put(self,request):
        student = Student.objects.get(user=request.user)
        serializer = CustomerUpdateSerializer(
            instance=student, data=request.data, 
            user=request.data['user'], partial=True
        )
        if serializer.is_valid():
            serializer.save()
            response = {"resp_code":1,
                        "message":"Profile updated successfully.",
                        "data":serializer.data
                        }
        else:
            response = {"resp_code":0,
                        "message":serializer.errors,
                        "data":{}
                        }
        return Response(response)
    

class CourseListView(APIView):
    def get(self,request):
        pass

        try:
            courses = Course.objects.filter(flag=True)
        except:
            return Response(
                {
                    "message":"Error fetching data",
                    "resp_code":0
                }
            )
        else:
            serializer = CourseSerializer(courses)
            return Response(
                {
                    "message":"success",
                    "resp_code":1,
                    "data":serializer.data
                }
            )




