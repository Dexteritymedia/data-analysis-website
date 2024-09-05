from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
 
class User(AbstractUser):

    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )
    
    gender = models.CharField(max_length=30, blank=True, null=True, default="F", choices=GENDER)

    def __str__(self):
        if self.username == None:
            return f'Username: Anonymous Gender: {self.gender}'
        return f'Username: {self.username} Gender: {self.gender}'
