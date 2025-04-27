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
    def get(self, request):
        try:
            courses = Course.objects.filter(flag=True)
            search = request.GET.get('search')
            # category = request.GET.get('category')

            if search:
                courses = courses.filter(title__icontains=search)

            # if category:
            #     courses = courses.filter(category__name__icontains=category)

        except Exception as e:
            return Response(
                {
                    "message": "Error fetching data",
                    "resp_code": 0,
                    "error": str(e) 
                }
            )
        else:
            serializer = CourseSerializer(courses, many=True)
            return Response(
                {
                    "message": "success",
                    "resp_code": 1,
                    "data": serializer.data
                }
            )
        
        
class ChapterListView(APIView):
    def get(self, request):
        course_id = request.GET.get("course_id")
        search = request.GET.get('search')

        if not course_id:
            return Response(
                {"message": "Course ID is required", "resp_code": 0},
                status=400
            )

        try:
            if not Course.objects.filter(id=course_id, flag=True).exists():
                return Response(
                    {"message": "Course not found", "resp_code": 0}
                )
            
            chapters = Chapter.objects.filter(course_id=course_id, flag=True)

            if search:
                chapters = chapters.filter(title__icontains=search)

            serializer = ChapterSerializer(chapters, many=True)
            return Response(
                {
                    "message": "success",
                    "resp_code": 1,
                    "data": serializer.data
                }
            )
        
        except Exception as e:
            return Response(
                {
                    "message": f"An error occurred: {str(e)}",
                    "resp_code": 0
                }
            )




