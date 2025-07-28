from django.db import models
from baseapp.models import BasemodelMixin
from backend.models import CustomUser

# Create your models here.
class Batch(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)
    code = models.CharField(unique=True,max_length=200)

    def __str__(self):
        return f"{self.name} {self.code}"

class Student(BasemodelMixin):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    group_code = models.CharField(max_length=200,null=True,blank=True)
    profile_image = models.ImageField(null=True,blank=True,upload_to='students')
    student_bio = models.TextField(null=True,blank=True)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
    package = models.ForeignKey('Package', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    community = models.ManyToManyField('Community', blank=True)  ## add related name if needed

    # def __str__(self):
    #     return f"{self.user}"


class Chapter(BasemodelMixin):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='chapters')
    description = models.TextField(null=True,blank=True)
    duration = models.IntegerField(null=True,blank=True)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.title}"

class SubChapters(BasemodelMixin):
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,related_name="sub_chapter")
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    video = models.FileField(upload_to='subchapters/videos')
    thumbnail = models.ImageField(upload_to='chapters/subchapters')
    duration = models.IntegerField(null=True,blank=True)
    order = models.IntegerField()

    def get_queryset(self):
        return SubChapters.objects.all().order_by('order')
    

class Features(BasemodelMixin):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

class Package(BasemodelMixin):
    title = models.CharField(max_length=200)
    thumbnail =  models.ImageField(upload_to='packages')
    price = models.FloatField(default=0)
    offer = models.FloatField(default=0)
    features= models.ManyToManyField(Features,related_name="package_features")

class Purchase(BasemodelMixin):
    payment_status = [
        ("success","Success"),
        ("in_progress","In progress"),
        ("failed","Failed")
    ]
    student = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,related_name='purchased_student')
    package = models.ForeignKey(Package,on_delete=models.SET_NULL,related_name="purchased_package",null=True)
    payment_id = models.CharField(max_length=200)
    status = models.CharField(choices=payment_status)

    # def __str__(self):
    #     return f"{self.course_name.title} {self.get_status_display()}"

class SubChapterProgress(BasemodelMixin):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_progress')
    sub_chapter = models.ForeignKey(SubChapters, on_delete=models.CASCADE, related_name='sub_chapter_progress')
    is_completed = models.BooleanField(default=False)
    watched_duration = models.IntegerField(default=0)
    last_watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'sub_chapter')

    # def __str__(self):
    #     return f"{self.student.user} - {self.chapter.title} - {'Completed' if self.is_completed else 'In Progress'}"



class Community(models.Model):
    name = models.CharField(max_length=200)
    default_name = models.CharField(max_length=200,unique=True)
    type = models.CharField(max_length=50, choices=[("global", "Global"), ("batch", "Batch"), ("package", "Package")])
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(null=True,blank=True,upload_to='community')  

    def __str__(self):
        return f"{self.name} ({self.type})"
    

class Message(models.Model):
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.user.first_name}: {self.content[:20]}"


class MessageReadTracker(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    last_read_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'community')  # one entry per user per community

    def __str__(self):
        return f"{self.student.user.username} read up to {self.last_read_message.id if self.last_read_message else 'None'} in {self.community}"
    

