from django.db import models
from django.contrib.auth.models import User


class Roles(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    role = models.ForeignKey(Roles, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'profile_pictures/', default='profile_pictures/default.png')
    bio = models.TextField(default="No bio provided")

    def __str__(self):
        return self.user.username

    
class Doctor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete = models.CASCADE)
    specialty = models.CharField(max_length = 100)
    license_number = models.CharField(max_length = 100)
    charge_per_hour = models.DecimalField(max_digits = 15, decimal_places=2, default = 0.00)
    available_days = models.CharField(max_length = 100, default = "Monday - Friday")
    available_from = models.TimeField(default='08:00:00')
    available_to = models.TimeField(default='17:00:00')

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.specialty}"