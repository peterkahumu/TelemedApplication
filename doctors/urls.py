from django.urls import path
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('update-doctor-info/', UpdateDoctorInfo.as_view(), name = "update_doctor_info"),
    path('requested_appointments', AppointmentRequest.as_view(), name = 'requested_appointments'),
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)