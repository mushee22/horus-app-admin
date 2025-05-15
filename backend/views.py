from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
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
            return redirect('dashboard')
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
    
    
class StudentCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'student/create_student.html'
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['batches'] = Batch.objects.all()
        return context
    
    def post(self,request):
        try:
            batch = Batch.objects.get(
                id=request.POST.get("batch")
            )
        except:
            messages.error(request,"Batch does not exist.")
            return redirect('list_student')
        
        try:
            case_study = CaseStudy.objects.create(
                heading = request.POST.get("heading"),
                image = request.FILES.get("image"),
                inner_image = request.FILES.get("inner_image"),
                client_overview = request.POST.get("client_overview"),
                client_says = request.POST.get("client_says"),
                challenge_description = request.POST.get("challenge_description"),
                solution_description = request.POST.get("solution_description"),
                result_description = request.POST.get("result_description"),
                country = country
            )
            case_study.industries.set(request.POST.getlist("industries"))
            case_study.save()
            messages.success(request,"Case studies created")
            return redirect('case_studies')

        except Exception as e:
            messages.error(request,"Failed to create Case studies")
            return redirect('case_studies')
        
        
# class CaseStudiesUpdateView(LoginRequiredMixin,DetailView):
#     model = CaseStudy
#     template_name = 'casestudy/update_case_study.html'
#     context_object_name = 'case_study'
        
#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         context['countries'] = Country.objects.filter(
#             is_archived=False
#         )
#         industries = Industry.objects.filter(
#             is_archived=False
#         )
#         current = context["case_study"].industries.values_list("id","industry_name")
#         context['industries']= industries
#         context['indus'] = list(current)
#         return context
    
#     def post(self,request,*args,**kwargs):
#         try:
#             country = Country.objects.get(
#                 id=request.POST.get("country")
#             )
#         except:
#             messages.error(request,"Country does not exist.")
#             return redirect('case_studies')
        
#         if self.model.objects.filter(id=kwargs['pk']).exists():
#             case_study = self.model.objects.get(id=kwargs['pk'])
#             case_study.heading = request.POST.get("heading")
#             case_study.image = request.FILES.get("image",case_study.image)
#             case_study.inner_image = request.FILES.get("inner_image",case_study.inner_image)
#             case_study.client_overview = request.POST.get("client_overview")
#             case_study.client_says = request.POST.get("client_says")
#             case_study.challenge_description = request.POST.get("challenge_description")
#             case_study.solution_description = request.POST.get("solution_description")
#             case_study.result_description = request.POST.get("result_description")
#             case_study.country = country
#             case_study.industries.set(request.POST.getlist("industries"))
#             case_study.save()
#             messages.success(request,"Case studies Updated")
#             return redirect('case_studies')
#         else:
#             messages.error(request,"Failed to update Case studies")
#             return redirect('case_studies')
        

class StudentDeleteView(LoginRequiredMixin,DeleteMasterView):
    model = Student
    return_path = 'student_list'


# class CaseStudiesArchiveTogglerView(LoginRequiredMixin,MasterArchiveTogglerView):
#     model = CaseStudy
