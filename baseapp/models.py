from django.db import models

# Create your models here.

class BasemodelMixin(models.Model):
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    modified_time = models.TimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True