from django.db import models
from baseapp.models import BasemodelMixin
from backend.models import CustomUser

# Create your models here.
class StudentId(models.Model):
    code = models.CharField(unique=True,max_length=200)

class Student(BasemodelMixin):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    group_code = models.ForeignKey(StudentId,on_delete=models.SET_NULL,null=True,blank=True)
    profile_image = models.ImageField(null=True,blank=True,upload_to='students')

class Tutor(BasemodelMixin):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True,blank=True,upload_to='teachers')

class Course(BasemodelMixin):
    title = models.CharField(max_length=250)
    tutor = models.ManyToManyField(Tutor,related_name='courses')
    description = models.TextField(null=True,blank=True)
    price = models.FloatField(default=0)
    offer = models.FloatField(default=0)
    thumbnail =  models.ImageField(upload_to='courses')

class Chapter(BasemodelMixin):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='course_chapter')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    video_url = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/chapters')
    duration = models.IntegerField()
    order = models.IntegerField()

class Purchase(BasemodelMixin):
    payment_status = [
        ("success","Success"),
        ("in_progress","In progress"),
        ("failed","Failed")
    ]
    course_name = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,related_name='purchased_course')
    student = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,related_name='purchased_student')
    payment_id = models.CharField(max_length=200)
    status = models.CharField(choices=payment_status)




