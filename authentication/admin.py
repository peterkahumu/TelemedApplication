from django.contrib import admin
from .models import *

admin.site.register(Roles)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'bio', 'image']
    list_filter  = ['role']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'specialty', 'license_number']
    list_filter  = ['specialty']
