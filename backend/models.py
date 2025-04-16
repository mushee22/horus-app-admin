from django.db import models
from django.contrib.auth.models import Group,AbstractUser
from baseapp.models import BasemodelMixin

# Create your models here.

class Role(Group):
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    flag = models.BooleanField(default=True)


class CustomUser(AbstractUser,BasemodelMixin):
    phone = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=True)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return str(self.username)




