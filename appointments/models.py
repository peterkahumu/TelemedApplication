from django.db import models
from authentication.models import User, Doctor, UserProfile

# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    # status: Pending, Approved, Rejected, Cancelled
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " - " + self.doctor.user_profile.user.first_name + " " + self.doctor.user_profile.user.first_name + " - " + str(self.date) + " " + str(self.time) + " - " + self.status