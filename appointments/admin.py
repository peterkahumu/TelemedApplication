from django.contrib import admin
from .models import Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'date', 'time', 'status']
    list_filter = ['status']
    search_fields = ['user__first_name', 'user__last_name', 'doctor__user_profile__user__first_name', 'doctor__user_profile__user__last_name', 'date', 'time', 'status']
    ordering = ['date', 'time']