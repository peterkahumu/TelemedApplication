from django.shortcuts import render, redirect
from django.views import View
from authentication.models import Doctor, UserProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class BookAppointment(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        user = request.user
        doctors = Doctor.objects.all()   
        context = {
            'doctors': doctors,
        }

        return render(request, 'patients/book_appointment.html', context)