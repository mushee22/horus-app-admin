from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import uuid
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# Internal funcions imports
from web.serializers import *
from baseapp.mixins import LoginRequiredMixin
import pandas as pd


# Create your views here.

def mark_messages_read(last_message,student,community):
    """
    Marks the given message as the last read by the student in the specified community.
    Creates or updates the read tracker entry.
    """

    print("hello comes the last message id",last_message.id,student,community)
    MessageReadTracker.objects.update_or_create(
        student=student,
        community=community,
        defaults={'last_read_message': last_message}
    )


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
    
    
class   CustomerProfileView(LoginRequiredMixin,APIView):
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


class MessageCreateView(APIView):

    def post(self,request):
        user_id = request.data.get('user')
        community_id= request.data.get('community')
        content = request.data.get('content')
        image_url = request.data.get('image_url',None)

        print("hello comes the image url",image_url)

        try:
            community = Community.objects.get(id=community_id)
            student = Student.objects.get(user__id=user_id)
            Message.objects.create(
                sender = student, 
                community=community,
                content = content,
                image = image_url
            )
            return Response({'resp_code':1,'message':"Success"})
        except (Community.DoesNotExist, Student.DoesNotExist):
            return Response({'resp_code': 0, 'message': "Community or Student not found"})
        except Exception as e:
            return Response({'resp_code':0,'message':"failed to create message"})


class Chatlistview(LoginRequiredMixin,APIView):

    def get(self, request):
        user = request.user

        if user.is_admin:
            communities = Community.objects.all()
        else:
            try:
                student = Student.objects.get(user=user)
                communities = student.community.all()
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found."}, status=404)
            
        serializer = CommunitySerializer(
            communities, many=True,
            context={'student': student}
        )
        return Response({"resp_code":1,"data":serializer.data,"message":"succes"})
        

class ListMessagesView(APIView):

    class MessagePagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 100
    
    def post(self,request):
        user = int(request.data.get('user'))
        community_id = request.data.get('community_id')
        try:
            student = Student.objects.get(user=user)
            community = Community.objects.get(id=community_id)
            messages = Message.objects.filter(
                community=community
            ).select_related('sender').order_by('-id')
            last_message = messages.last()

            # Paginate
            paginator = self.MessagePagination()
            page = paginator.paginate_queryset(messages, request)
            page = list(page)[::-1]

            page = list(page)[::-1]

            serializer = MessageSerializer(page,many=True)
            arranged_messages = self.arranage_message_by_date(serializer.data)
            community_serializer = CommunityMiniSerializer(community)
            if last_message:
                mark_messages_read(last_message,student,community)
            # Mark messages read for current student (based on last in this page)
            # if page:
            #     mark_messages_read(page[-1], student, community)

            return paginator.get_paginated_response({
                'resp_code':1,
                'data':arranged_messages,
                'community': community_serializer.data,
                'message':"Success"
            })
        except Exception as e:
            return Response({'resp_code':0,'message':str(e)})

    def arranage_message_by_date(self,data):
        message_date_list = []
        for message in data:
            if message['date'] not in message_date_list:
                message_date_list.append(message['date'])
        df = pd.DataFrame(data)
        arranged_list = []
        message_data = {}
        for date in message_date_list:
            message_data['date'] = date
            messages = df.loc[df['date']==date]
            # messages = messages.sort_values(by='id', ascending=True)
            message_list = messages.to_dict(orient='records')
            message_data['messages'] = message_list
            arranged_list.append(message_data)
            message_data = {}
        
        return arranged_list


@csrf_exempt
def upload_chat_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        filename = f"{uuid.uuid4().hex}_{image.name}"

        # Open image using Pillow
        img = Image.open(image)

        # Convert image to RGB if it's not already
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Create buffer to compress image
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=70, optimize=True)  # You can tweak quality value
        buffer.seek(0)

        # Save compressed image to disk
        save_path = os.path.join(settings.MEDIA_ROOT, "chat_images", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb+") as f:
            f.write(buffer.read())

        return JsonResponse({"image_url": f"chat_images/{filename}"})

    return JsonResponse({"error": "Invalid request"}, status=400)


class CommunityMembers(APIView):
    """
    This function fetches all the members in the community and sends their id as
    a list. This is for managing Live chat notification in the community.
    """
    def get(self, request, community_id):
        try:
            user_ids = Student.objects.filter(
                community__id=community_id
            ).values_list("user_id",flat=True)
            return Response({'resp_code':1,'user_ids':user_ids,'message':"Success"})
        except Community.DoesNotExist:
            return Response({'resp_code':0,'message':"Community not found"})
        except Exception as e:
            return Response({'resp_code':0,'message':str(e)})