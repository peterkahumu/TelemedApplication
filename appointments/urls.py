from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('book_appointment/', BookAppointment.as_view(), name = 'book_appointment'),
    path('edit_appointment/<int:id>', EditAppointment.as_view(), name = 'edit_appointment'),
    path('delete_appointment/<int:id>', DeleteAppointment.as_view(), name = 'delete_appointment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)