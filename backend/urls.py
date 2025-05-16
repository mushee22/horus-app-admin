from django.urls import path
from backend.views import *   #AdminView,LoginView,CaseStudiesListView

urlpatterns = [
    # Login Logout
    path('login/',LoginView.as_view(),name="admin_login"),
    path('logout/', logout_view, name='logout'),
    # Students
    path('',StudentListView.as_view(),name="student_list"),
    path('student/create/',StudentCreateView.as_view(),name="create_student"),
    path('student/update/<int:pk>/',StudentUpdateView.as_view(),name="update_student"),
    path('student/delete/',StudentDeleteView.as_view(),name="delete_student"),
    # Chapter
    path('chapter',ChapterListView.as_view(),name="chapter_list"),
    path('chapter/create/',ChapterCreateView.as_view(),name="create_chapter"),
    path('chapter/update/<int:pk>/',ChapterUpdateView.as_view(),name="update_chapter"),
    path('chapter/delete/',ChapterDeleteView.as_view(),name="delete_chapter"),

]