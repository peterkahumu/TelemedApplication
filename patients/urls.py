from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

# create your urls here
urlpatterns = [
    path('appointments/', PatientAppointments.as_view(), name="patient_appointments"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)