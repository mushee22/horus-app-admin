from django.urls import path
from backend.views import *   #AdminView,LoginView,CaseStudiesListView

urlpatterns = [
    # Login Logout
    path('login/',LoginView.as_view(),name="admin_login"),
    path('logout/', logout_view, name='logout'),
    # Students
    path('',StudentListView.as_view(),name="student_list"),
    path('student/create/',StudentCreateView.as_view(),name="create_student"),
    path('student/delete/',StudentDeleteView.as_view(),name="delete_student"),

]