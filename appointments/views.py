from django.shortcuts import render, redirect
from django.views import View
from authentication.models import Doctor, UserProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import Appointment
from datetime import datetime, timedelta


# Create your views here.
class BookAppointment(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def return_with_context(self, request, context):
        return render(request, 'appointments/book_appointment.html', context)

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

        return self.return_with_context(request, context)
    
    def post(self, request):
        context = {
            'values': request.POST
        }

        user = request.user
        doctor_id = request.POST['doctor_id']
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        appointment_reason = request.POST['appointment_reason']

        # pagination to be included in the context
        doctors = Doctor.objects.all()
        paginator = Paginator(doctors, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context['doctors'] = doctors
        context['page_obj'] = page_obj

        # validate the data
        if not doctor_id or not appointment_date or not appointment_time or not appointment_reason:
            messages.error(request, 'All fields are required')
            return self.return_with_context(request, context)
        
        # convert the 24 hr apointment time from string to datetime
        try:
            appointment_time = datetime.strptime(appointment_time, '%H:%M').time()
        except:
            messages.error(request, 'Invalid appointment time format. User HH:MM')
            return self.return_with_context(request, context)
        
        # convert the appointment date from string to datetime
        try:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        except:
            messages.error(request, 'Invalid appointment date')
            return self.return_with_context(request, context)
        
        # ensure that the appointment date is not in the past
        if appointment_date < datetime.now().date():
            messages.error(request, 'Invalid appointment date')
            return self.return_with_context(request, context)
        
        try: 
            doctor = Doctor.objects.get(id=doctor_id)
            start_time = doctor.available_from
            end_time = doctor.available_to # Doctors available time.
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor does not exist')
            return self.return_with_context(request, context)
        except Exception as e:
            messages.error(request, 'Error occurred while Fetching the doctor')
            return self.return_with_context(request, context)
        
        # ensure that the doctor does not have an active appointment on selected date and time. (Start_time + 1 hour)
        try:
            appointment = Appointment.objects.get(doctor=doctor, date=appointment_date)
            appointment_stop = datetime.combine(appointment_date, appointment.time) + timedelta(hours=1)
            appointment_stop = appointment_stop.time()
            if appointment.time <= appointment_time <= appointment_stop:
                messages.error(request, f"Doctor {doctor.user_profile.user.first_name} already has an appointment at {appointment.time} to {appointment_stop} on {appointment_date}. Please select a different time or date.")
                return self.return_with_context(request, context)
        except Appointment.DoesNotExist:
            pass
        except Exception as e:
            messages.error(request, f'Error occurred while checking the doctor appointment, {e}')
            return self.return_with_context(request, context)                             
        try:
            if appointment_time < start_time or appointment_time > end_time:
                messages.error(request, f"Doctor {doctor.user_profile.user.first_name} is only available from {start_time} to {end_time}. Please select a time within the range or try another doctor.")
                return self.return_with_context(request, context)
            
            appointment = Appointment(user=user, doctor=doctor, date=appointment_date, time=appointment_time, reason=appointment_reason, status='Pending')
            appointment.save()
            messages.success(request, 'Appointment booked successfully')
            return redirect('patient_appointments')
        except:
            messages.error(request, "Error occurred while booking the appointment.")
            return self.return_with_context(request, context)
