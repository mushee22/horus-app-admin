from django.urls import path
from web.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    # login
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # student
    path('registration/', CustomerRegistrationView.as_view(), name='student-registration'),
    path('student-profile/', CustomerProfileView.as_view(), name='student-profile'),
    path('student-profile/update/', ProfileUpdateView.as_view(), name='student-profile-update'),
    # Courses 
    path('list-courses/', CourseListView.as_view(), name='all-courses'),

]
