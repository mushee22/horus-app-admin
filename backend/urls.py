from django.urls import path
from backend.views import *   #AdminView,LoginView,CaseStudiesListView

urlpatterns = [
    # Login Logout
    path('login/',LoginView.as_view(),name="admin_login"),
    path('logout/', logout_view, name='logout'),

    # Admin
    path('users', AdminListView.as_view(), name="admin_user_list"),
    path('users/create/',CreateAdminView.as_view(),name="create_admin_user"),
    path('users/update/<int:pk>/',AdminUpdateView.as_view(),name="update_admin_user"),
    path('users/delete', AdminDeleteView.as_view(), name="delete_admin_user"),

    # Role
    path('role',RoleListView.as_view(),name="role_list"),
    path('role/create/',RoleCreateView.as_view(),name="create_role"),

    # Students
    path('',StudentListView.as_view(),name="student_list"),
    path('student/create/',StudentCreateView.as_view(),name="create_student"),
    path('student/update/<int:pk>/',StudentUpdateView.as_view(),name="update_student"),
    path('student/delete/',StudentDeleteView.as_view(),name="delete_student"),
    # Chapter
    path('chapter',ChapterListView.as_view(),name="chapter_list"),
    path('chapter/create/',ChapterCreateView.as_view(),name="create_chapter"),
    path('chapter/update/<int:pk>/',ChapterUpdateView.as_view(),name="update_chapter"),
    path('chapter/delete',ChapterDeleteView.as_view(),name="delete_chapter"),
    #Sub Chapter
    path('sub-chapter',SubChapterListView.as_view(),name="sub_chapter_list"),
    path('sub-chapter/create/',SubChapterCreatView.as_view(),name="create_sub_chapter"),
    path('sub-chapter/update/<int:pk>/',SubChapterUpdateView.as_view(),name="update_sub_chapter"),
    path('sub-chapter/delete',SubChapterDeleteView.as_view(),name="delete_sub_chapter"),
    path('sub-chapter/upload-status',UploadStatusView.as_view(),name="upload_status"),
    #batch
    path('batch',BatchListView.as_view(),name="batch_list"),
    path('batch/create/',BatchCreateView.as_view(),name="create_batch"),
    path('batch/update/<int:pk>/',BatchUpdateView.as_view(),name="update_batch"),
    path('batch/delete',BacthDeleteView.as_view(),name="delete_batch"),
    path('batch/<int:pk>/student',BatchStudentListView.as_view(),name="list_batch_student"),
    #Package
    path('package',PackageListView.as_view(),name="package_list"),
    path('package/create/',PackageCreateView.as_view(),name="create_package"),
    path('package/update/<int:pk>/',PackageUpdateView.as_view(),name="update_package"),
    path('package/delete',PackageDeleteView.as_view(),name="delete_package"),
    path('package/<int:pk>/student',PackageStudentListView.as_view(),name="list_package_student"),
]
