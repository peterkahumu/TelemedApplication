from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    role = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'profile_pictures/', default='profile_pictures/default.png')
    bio = models.TextField(default="No bio provided")

    def __str__(self):
        return self.user.username
    

class Roles(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name