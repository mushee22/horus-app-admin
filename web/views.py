from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
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
            return Response({
                "resp_code":1,
                "message":"Profile updated successfully.",
                "data":serializer.data
            },
            status=status.HTTP_200_OK
            )

        else:
            return Response({
               "resp_code":0,
               "message":serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
            )


class UpdateUserPassword(LoginRequiredMixin, APIView):
    def put(self, request):
        serializer = CustomerPasswordUpdateSerializer(
            data=request.data, 
            context={'request': request}
        )  
        if serializer.is_valid():
            serializer.save()
            return Response({
                "resp_code":1,
                "message":"Password updated successfully.",
                "data":serializer.data
            },
            status=status.HTTP_200_OK
            )

        else:
            return Response({
               "resp_code":0,
               "message":serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
            )
       
        
class ChapterListView(LoginRequiredMixin,APIView):
    def get(self, request):
        search = request.GET.get('search')

        try:
            chapters = Chapter.objects.filter(is_active=True)

            if search:
                chapters = chapters.filter(title__icontains=search)

            serializer = ChapterSerializer(chapters, many=True,context={'request': request})
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
        

class SubChapterListView(LoginRequiredMixin, APIView):
    def get(self, request, slug):
        try:
            chapter = Chapter.objects.get(id=slug,is_active=True)
        except Chapter.DoesNotExist:
            return Response({
                "message": "Chapter not found",
                "resp_code": 0
            }, status=404)

        subchapters = chapter.sub_chapter.all().order_by('order')  # Optional ordering
        serializer = SubChapterSerializer(subchapters, many=True, context={'request': request})

        return Response({
            "message": "success",
            "resp_code": 1,
            "chapter": chapter.title,
            "data": serializer.data
        })


class SubChapterDetailView(LoginRequiredMixin, APIView):
    def get(self, request, slug):
        try:
            subchapter = SubChapters.objects.get(id=slug)
        except SubChapters.DoesNotExist:
            return Response({
                "message": "Subchapter not found",
                "resp_code": 0
            }, status=404)

        serializer = SubChapterDetailSerializer(subchapter, context={'request': request})
        return Response({
            "message": "success",
            "resp_code": 1,
            "data": serializer.data
        })
    

class UpdateSubChapterProgressView(LoginRequiredMixin, APIView):
    def post(self, request):
        sub_chapter_id = request.data.get('sub_chapter_id')
        is_completed = request.data.get('is_completed', False)
        watched_duration = request.data.get('watched_duration', 0)

        if sub_chapter_id is None:
            return Response({
                "message": "sub_chapter_id is required",
                "resp_code": 0
            }, status=400)

        try:
            student = Student.objects.get(user=request.user)
            sub_chapter = SubChapters.objects.get(id=sub_chapter_id)
        except Student.DoesNotExist:
            return Response({"message": "Student not found", "resp_code": 0}, status=404)
        except SubChapters.DoesNotExist:
            return Response({"message": "Subchapter not found", "resp_code": 0}, status=404)

        progress, created = SubChapterProgress.objects.get_or_create(
            student=student,
            sub_chapter=sub_chapter,
            defaults={
                'is_completed': is_completed,
                'watched_duration': watched_duration
            }
        )

        if created:
            return Response({
                "message": "Progress created",
                "resp_code": 1
            })

        progress.watched_duration = watched_duration
        if not progress.is_completed:
            progress.is_completed = is_completed
        progress.save()


        return Response({
            "message": "Progress updated",
            "resp_code": 1
        })
    
    
class UpdateStudentProfileImageView(LoginRequiredMixin, APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({"message": "Student not found", "resp_code": 0}, status=404)

        profile_image = request.FILES.get('profile_image')
        if not profile_image:
            return Response({"message": "No image file provided", "resp_code": 0}, status=400)

        student.profile_image = profile_image
        student.save()

        return Response({
            "message": "Profile image updated successfully",
            "resp_code": 1,
            "image_url": request.build_absolute_uri(student.profile_image.url)
        }, status=200)
    
    
class PackageListView(APIView):
    def get(self, request):
        packages = Package.objects.all()
        serializer = PackageSerializer(packages, many=True, context={'request': request})
        return Response({
            "message": "success",
            "resp_code": 1,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class TotalProgressView(LoginRequiredMixin, APIView):
    def get(self, request):
        try:
            user = request.user
            student = Student.objects.get(user=user)

            total_subchapters = SubChapters.objects.count()
            completed_subchapters = SubChapterProgress.objects.filter(
                student=student, is_completed=True
            ).count()

            last_watched_sub_chapter = SubChapterProgress.objects.filter(
                student=student
            ).order_by('-last_watched_at').first()

            if last_watched_sub_chapter:
                sub_chapter = SubChapters.objects.get(id=last_watched_sub_chapter.sub_chapter.id)
                serializer = SubChapterDetailSerializer(sub_chapter, context={'request': request})


            return Response({
                "message": "success",
                "resp_code": 1,
                "data": {
                    "total_subchapters": total_subchapters,
                    "completed_subchapters": completed_subchapters,
                    "last_watched_sub_chapter": serializer.data if last_watched_sub_chapter else None
                }
            }, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({
                "message": "Student profile not found",
                "resp_code": 0
            }, status=status.HTTP_404_NOT_FOUND)


