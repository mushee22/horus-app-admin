from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect,get_object_or_404
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View,TemplateView,ListView,DetailView,UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q,Sum,Case,When,IntegerField

# Models Import
from web.models import *


# Create your views here.
class DeleteMasterView(View):
    '''
        To soft delete the record of a model. the model and redirecting url
        will be taken from the curresponding view 
        method: get
        params: pk - the id of the record to delete
    '''
    def get(self,request):
        pk = request.GET.get('pk')
        args = request.GET.get('args')
        if self.model.objects.filter(id=pk).exists():
            queryset = self.model.objects.get(id=pk)
            # queryset.is_deleted = True
            try:
                queryset.delete()
                messages.success(request,"Deleted succesfully")
            except:
                messages.error(request,"Failed to delete")
        else:
            messages.error(request,"Object doesn't exist")

        if args:
            return redirect(self.return_path,args)
        else:
            return redirect(self.return_path)
        

class MasterArchiveTogglerView(View):
    '''
        To archive or unarchive any of the record of the table.
        method: GET
        params:
            - pk: primeary key of the record
    '''
    def get(self,request):
        obj = self.model.objects.get(id=request.GET.get('pk'))
        if obj.is_archived:
            obj.is_archived = False
        else:
            obj.is_archived = True
        try:
            obj.save()
            response = {'resp_code':1}
        except:
            response = {'resp_code':0}
        return JsonResponse(response)


class LoginView(TemplateView):
    template_name = "login.html"
    
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('student_list')
        else:
            messages.error(request,"User not found")
            return redirect('admin_login')

def logout_view(request):
    auth.logout(request)
    return redirect('admin_login')


class AdminView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'

    def count_setting(self,count):
        if count>999:
            return '999+'
        else:
            return count
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['purchase'] = PurchaseForm.objects.all().order_by('-id')[:7]
        # contact_count = ContactMessage.objects.all().count()
        # purchase_count = PurchaseForm.objects.all().count()

        # context['contact_count'] = self.count_setting(contact_count)
        # context['purchase_count'] = self.count_setting(purchase_count)
        # context['total_count'] = self.count_setting(contact_count+purchase_count)
        return context
    

class StudentListView(LoginRequiredMixin,ListView):
    model = Student
    template_name = 'student/list_student.html'
    context_object_name = 'context_data'
    paginate_by = 10

    def get_queryset(self):
        queryset =  super().get_queryset()

        search = self.request.GET.get("search")
        sort = self.request.GET.get("sort")
        category_filter = self.request.GET.get("filter")

        if search:
            queryset = queryset.filter(
                Q(user__first_name__istartswith=search)|
                Q(user__last_name__istartswith=search)
            )
        
        if sort == "oldest":
            queryset = queryset.order_by('id')
        else:
            queryset = queryset.order_by('-id')

        # if category_filter:
        #     queryset = queryset.filter(category=category_filter)

        return queryset
    

class StudentCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'student/create_student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batches'] = Batch.objects.all()
        return context

    def post(self, request):
        try:
            batch = Batch.objects.get(id=request.POST.get("batch"))
        except Batch.DoesNotExist:
            messages.error(request, "Batch does not exist.")
            return redirect('student_list')

        try:
            # Create user and hash the password properly
            user = CustomUser(
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                username=request.POST.get("email"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone")
            )
            user.set_password(request.POST.get("password"))  # ✅ Hash the password
            user.save()

            # Handle profile image properly
            profile_image = request.FILES.get("profile_image")

            Student.objects.create(
                user=user,
                profile_image=profile_image,
                batch=batch,
                start_date=request.POST.get("start_date"),
                end_date=request.POST.get("end_date"),
                student_bio=request.POST.get("student_bio")
            )

            messages.success(request, "Student created successfully.")
            return redirect('student_list')

        except Exception as e:
            messages.error(request, f"Failed to create student: {str(e)}")
            return redirect('student_list')

        
        
class StudentUpdateView(LoginRequiredMixin, DetailView):
    template_name = 'student/update_student.html'
    model = Student
    context_object_name ='context_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # student_id = self.kwargs.get('pk')  # Assuming URL is like path('student/update/<int:pk>/')
        # student = get_object_or_404(Student, pk=student_id)

        # context['student'] = student
        # context['user'] = student.user
        context['batches'] = Batch.objects.all()
        return context

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        user = student.user

        try:
            batch = Batch.objects.get(id=request.POST.get("batch"))
        except Batch.DoesNotExist:
            messages.error(request, "Batch does not exist.")
            return redirect('student_list')

        try:
            # Update user details
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.username = request.POST.get("email")
            user.phone = request.POST.get("phone")

            # Only update password if provided
            new_password = request.POST.get("password")
            if new_password:
                user.set_password(new_password)

            user.save()

            # Update student details
            student.batch = batch
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            if start_date:
               student.start_date = start_date
            if end_date:
               student.end_date = end_date

            student.save()

            messages.success(request, "Student details updated successfully.")
            return redirect('student_list')

        except Exception as e:
            messages.error(request, f"Failed to update student: {str(e)}")
            return redirect('student_list')
        

class StudentDeleteView(LoginRequiredMixin,DeleteMasterView):
    model = Student
    return_path = 'student_list'



# *********************************************************************************


class ChapterListView(LoginRequiredMixin,ListView):
    model = Chapter
    template_name = 'chapter/list_chapter.html'
    context_object_name = 'context_data'
    paginate_by = 10

    def get_queryset(self):
        queryset =  super().get_queryset()

        search = self.request.GET.get("search")
        sort = self.request.GET.get("sort")
        category_filter = self.request.GET.get("filter")

        if search:
            queryset = queryset.filter(
                Q(title__istartswith=search))
        
        if sort == "oldest":
            queryset = queryset.order_by('id')
        else:
            queryset = queryset.order_by('-id')

        # if category_filter:
        #     queryset = queryset.filter(category=category_filter)

        return queryset
    
class ChapterCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'chapter/create_chapter.html'

    def post(self, request):

        try:
            Chapter.objects.create(
                title=request.POST.get("title"),
                thumbnail=request.FILES.get("thumbnail"),
                description=request.POST.get("description"),
                order=request.POST.get("order"),
            )
            messages.success(request, "Chapter created successfully.")
            return redirect('chapter_list')

        except Exception as e:
            messages.error(request, f"Failed to create student: {str(e)}")
            return redirect('chapter_list')
   
class ChapterUpdateView(LoginRequiredMixin, DetailView):
    template_name = 'chapter/update_chapter.html'
    model = Chapter
    context_object_name ='context_data'


    def post(self, request, pk):
        chapter = get_object_or_404(Chapter, pk=pk)

        try:
            # Update user details
            chapter.title=request.POST.get("title")
            chapter.description=request.POST.get("description")
            chapter.order=request.POST.get("order")

            # Update thumbnail if a new one is uploaded
            if request.FILES.get("thumbnail"):
                chapter.thumbnail = request.FILES.get("thumbnail")

            chapter.save()

            messages.success(request, "Student details updated successfully.")
            return redirect('chapter_list')

        except Exception as e:
            messages.error(request, f"Failed to update student: {str(e)}")
            return redirect('chapter_list')
        
class ChapterDeleteView(LoginRequiredMixin,DeleteMasterView):
    model = Chapter
    return_path = 'chapter_list'

#*********************************************************************************

class BatchListView(LoginRequiredMixin,ListView):
    model = Batch
    template_name = 'batch/list_batch.html'
    context_object_name = 'context_data'
    paginate_by = 10

class BatchCreateView(LoginRequiredMixin, TemplateView):

    template_name = 'batch/create_batch.html'

    def post(self, request):
        try:
            Batch.objects.create(
                name=request.POST.get("name"),
                code=request.POST.get("code"),
            )
            messages.success(request, "Batch created successfully.")
            return redirect('batch_list')
        except Exception as e:
            messages.error(request, f"Failed to create batch: {str(e)}")
            return redirect('batch_list')

class BatchUpdateView(LoginRequiredMixin, DetailView):
    template_name = 'batch/update_batch.html'
    model = Batch
    context_object_name ='context_data'

    def post(self, request, pk):
        batch = get_object_or_404(Batch, pk=pk)
        try:
            batch.name = request.POST.get('name')
            batch.code = request.POST.get('code')
            batch.save()
            return redirect('batch_list')
        except Exception as e:
            messages.error(request, f"Failed to update student: {str(e)}")   
            return redirect('batch_list') 

class BacthDeleteView(LoginRequiredMixin,DeleteMasterView):
    model = Batch
    return_path = 'batch_list' 

#*************************************************************************
class SubChapterListView(LoginRequiredMixin, ListView):
    model = SubChapters
    template_name= 'sub-chapter/list_sub_chapter.html'
    context_object_name= "context_data"
    paginate_by = 10

class SubChapterCreatView(LoginRequiredMixin, TemplateView):
    template_name="sub-chapter/create_sub_chapter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = Chapter.objects.all()
        return context

    def post(self, request):
        try:
            
            chapter = Chapter.objects.get(id=request.POST.get("chapter"))

            SubChapters.objects.create(
                title=request.POST.get("title"),
                order=request.POST.get("order"),
                duration=request.POST.get("duration"),
                description=request.POST.get("description"),
                thumbnail=request.FILES.get("thumbnail"),
                video=request.FILES.get("video"),
                chapter=chapter
            )
            messages.success(request, "Sub Chapter created successfully.")
            return redirect('sub_chapter_list')
        except Exception as e:
            messages.error(request, f"Failed to create Sub Chapter: {str(e)}")   
            return redirect('sub_chapter_list') 
        
class SubChapterUpdateView(LoginRequiredMixin, DetailView):
    template_name = 'sub-chapter/update_sub_chapter.html'
    model = SubChapters
    context_object_name ='context_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = Chapter.objects.all()
        return context
    
    def post(self, request, pk):
        try:
            chapter = Chapter.objects.get(id=request.POST.get("chapter"))
        except Chapter.DoesNotExist:
            messages.error(request, "Chapter does not exist.")
            return redirect('sub_chapter_list')

        try:
            subChapter = get_object_or_404(SubChapters, pk=pk)
            subChapter.title = request.POST.get("title")
            subChapter.description = request.POST.get("description")
            subChapter.order=request.POST.get("order")
            subChapter.duration=request.POST.get("duration")
            subChapter.chapter = chapter

            if request.FILES.get("thumbnail"):
                subChapter.thumbnail = request.FILES.get("thumbnail")
            if request.FILES.get("video"):
                subChapter.video= request.FILES.get("video")

            subChapter.save()        

            messages.success(request, "Sub Chapter Updated successfully.")
            return redirect('sub_chapter_list')

        except Exception as e:
            messages.error(request, f"Failed to update: {str(e)}")
            return redirect('sub_chapter_list')
        
class SubChapterDeleteView(LoginRequiredMixin,DeleteMasterView):
    model = SubChapters
    return_path = 'sub_chapter_list'        