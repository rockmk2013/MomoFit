from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # add additional fields in here
    age = models.IntegerField(help_text='Enter age',default=20)
    sex = models.CharField(default='Male',max_length=5)
    height = models.IntegerField(default=160)
    weight = models.IntegerField(default=60)
    kcal = models.IntegerField(default=1500)

    def __str__(self):
        return self.email