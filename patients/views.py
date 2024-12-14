from django.shortcuts import render, render
from authentication.models import User, Doctor
from appointments.models import Appointment
from django.contrib import messages
from django.views import View

# create your views here
class PatientAppointments(View):
    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(user = user)

        context = {
            "appointments": appointments
        }

        return render(request, "patients/appointments.html", context)