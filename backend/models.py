from django.db import models
from django.contrib.auth.models import Group,AbstractUser,BaseUserManager
from baseapp.models import BasemodelMixin
from datetime import datetime,timedelta


# Create your models here.

class Role(Group):
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    flag = models.BooleanField(default=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The email field is required'))
        user = self.model(username=email,email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        email = self.normalize_email(email)
        user = self.model(username=email,email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser,BasemodelMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return str(self.username)
    
class OTP(models.Model):
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=200,null=True)
    otp = models.CharField(max_length=10)
    expire_time  = models.DateTimeField()

    def save(self,*args,**kwargs):
        expiry = datetime.now() + timedelta(minutes=2)
        self.expire_time = expiry
        super().save(*args,**kwargs)

class BackgroundTaskStatus(models.Model):
    model_id = models.CharField(max_length=200, unique=False)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'),  ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model_id} - {self.status}"

