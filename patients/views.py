from django.shortcuts import render, redirect
from authentication.models import User, Doctor
from appointments.models import Appointment
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from datetime import datetime

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

class EditAppointment(LoginRequiredMixin, View):
    def get(self, request, id):
        # ensure that the appointment belongs to the user.
        try:
            appointment = Appointment.objects.get(id = id)
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found")
            return redirect("patient_appointments")
        
        if appointment.user != request.user:
            messages.error(request, "Non-existent appointment. Please try again")
            return redirect("patient_appointments")
        
        context = {
            "appointment": appointment,
        }
        return render (request, "patients/edit_appointment.html", context)
    
    def post(self, request, id):
        try:
            appointment = Appointment.objects.get(id = id) # get the specific appoinment
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found")
            return redirect("patient_appointments")
        
        try:
            doctor = Doctor.objects.get(id = appointment.doctor.id)
        except Doctor.DoesNotExist:
            messages.error(request, "Trouble assigning doctor to appointment. Please try again or contact support")
            return redirect("patient_appointments")
        
        if appointment.user != request.user:
            messages.error(request, "Non-existent appointment. Please try again")
            return redirect("patient_appointments")
        
        appointment_date = request.POST['appointment_date']
        appointment_time = datetime.strptime(request.POST['appointment_time'], "%H:%M").time()
        appointment_reason = request.POST['appointment_reason']  
        
        if appointment_time < doctor.available_from or appointment_time > doctor.available_to:
            messages.error(request, "Doctor is only available from " + str(doctor.available_from) + " to " + str(doctor.available_to) + ". Please select a time within this range")
            return redirect("edit_appointment", id = id) 

        if not appointment_date:
            messages.error(request, "Appointment date is required")
            return redirect("edit_appointment", id = id)
        if not appointment_time:
            messages.error(request, "Appointment time is required")
            return redirect("edit_appointment", id = id)
        if not appointment_reason:
            messages.error(request, "Appointment reason is required")
            return redirect("edit_appointment", id = id)      

        if appointment.status == "Approved":
            messages.error(request, "Appointment has been approved and cannot be updated. Please contact the doctor for any changes")
            return redirect("edit_appointment", id = id) 
        
        try:
            appointment.date = appointment_date
            appointment.time = appointment_time
            appointment.reason = appointment_reason
            appointment.status = "Pending"
            appointment.save()
            messages.success(request, "Appointment updated successfully")
            return redirect("patient_appointments")
        except:
            messages.error(request, "Failed to update appointment, Please try again")
            return redirect("edit_appointment", id = id)
