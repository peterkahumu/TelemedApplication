from django.shortcuts import render, redirect
from django.views import View
from authentication.models import Doctor, UserProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

# Create your views here.
class BookAppointment(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        user = request.user
        doctors = Doctor.objects.all() 

        paginator = Paginator(doctors, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'doctors': doctors,
            'page_obj': page_obj
        }

        return render(request, 'appointments/book_appointment.html', context)