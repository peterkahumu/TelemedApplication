from django.shortcuts import render, redirect
from django.urls import reverse
from authentication.models import User, UserProfile, Doctor
from appointments.models import Appointment
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import Group
import datetime

# Create your views here.
class UpdateDoctorInfo(View, LoginRequiredMixin):
    login_url = 'login'
    redirect_field_name = 'next'

    def is_doctor(self, user):
        """Check if the user is a doctor."""
        return user.groups.filter(name = "doctors").exists()
    
    def redirect_profile(self):
         """Redirect the doctor to the update information form."""
         return redirect(f"{reverse('profile')}#doctor-info")
    
    def post(self, request):
        # check if user is a doctor
        user = request.user

        if not self.is_doctor(user):
            messages.error(request, "Unauthorized access. Request denied.")
            return redirect('home')
        
        user_profile = UserProfile.objects.get(user=user)
        doctor = Doctor.objects.get(user_profile = user_profile)

        if not user.userprofile.role.name == "Doctor": # ensure the user is a Doctor.
            messages.warning(request, "Unauthorized access request denied.")
            return redirect('home')
        
        specialty = request.POST['specialty']
        charge_per_hour = request.POST['charge_per_hour']
        available_days = request.POST['available_days']
        available_from = request.POST['available_from']
        availabe_to = request.POST['available_to']
        
        if not float(charge_per_hour).is_integer():
            messages.warning(request, 'The charge per hour must be a number.')
            return self.redirect_profile()
        
        if float(charge_per_hour) < 0:
            messages.warning(request, 'The charge per hour must be a positive number.')
            return self.redirect_profile()
        
        if not available_days:
            messages.warning(request, 'Please provide the days you are available.')
            return self.redirect_profile()
        if not available_from:
            messages.warning(request, 'Please provide the time you are available from.')
            return self.redirect_profile()
        if not availabe_to:
            messages.warning(request, 'Please provide the time you are available to.')
            return self.redirect_profile()
        
        if not specialty:
            messages.warning(request, 'Please provide your specialty.')
            return self.redirect_profile()
        
        # convert availabe to and from to time
        try:
            available_from = datetime.datetime.strptime(available_from, '%H:%M').time()
            availabe_to = datetime.datetime.strptime(availabe_to, '%H:%M').time()
        except Exception as e:
            messages.error(request, "An error occured while converting the time, please provide the time in the format HH:MM, using 24 hour format.")
            return self.redirect_profile()
        
        # ensure the available from is earlier than the available to
        if not available_from < availabe_to:
            messages.error(request, "The available from time must be earlier than the available to time.")
            return self.redirect_profile()
        
        if doctor.specialty == specialty and doctor.charge_per_hour == float(charge_per_hour) and doctor.available_days == available_days and doctor.available_from == available_from and doctor.available_to == availabe_to:
            messages.info(request, "No changes were made.")
            return redirect('profile')
        
        try:
            doctor.specialty = specialty
            doctor.charge_per_hour = charge_per_hour
            doctor.available_days = available_days
            doctor.available_from = available_from
            doctor.available_to = availabe_to
            doctor.save()

            messages.success(request, "Your proffesional information was updated successfully.")
            return redirect('profile')
        except Exception as e:
            messages.error(request, f"An error occured while updating your information, {e}")
            return self.redirect_profile()

class AppointmentRequest(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        user = request.user
        doctor = Doctor.objects.get(user_profile = user.userprofile)
        appointment = Appointment.objects.filter(doctor = doctor)
        context = {
            "appointment": appointment
        }

        return render(request, 'doctors/requested_appointments.html', context)
                
        
