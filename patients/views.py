from django.shortcuts import render, render
from authentication.models import User, Doctor
from appointments.models import Appointment
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

# create your views here
class PatientAppointments(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(user = user)

        paginator = Paginator(appointments, 10)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            "appointments": appointments,
            "page_obj": page_obj
        }

        return render(request, "patients/appointments.html", context)