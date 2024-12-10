from django.shortcuts import render, redirect
from django.views import View
from authentication.models import Doctor
from django.contrib import messages

# Create your views here.
class BookAppointment(View):
    def get(self, request):
        try:
            doctors = Doctor.objects.select_related('user_profile', 'user_profile__user').all()
        except Doctor.DoesNotExist:
             messages.error(request, 'No doctors available.')
             redirect('home')
        
        context = {
            'doctors': doctors
        }
        return render(request, 'patients/book_appointment.html')