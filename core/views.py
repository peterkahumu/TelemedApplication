from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UserProfile, User, Doctor
from django.contrib import messages
from django.urls import reverse
from appointments.models import Appointment
import datetime

# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, 'index.html')

class Home(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    
    def get(self, request):
        # get the upcoming appointment for the user (only 1) if any
        try:
            user = request.user
            appointment = Appointment.objects.filter(user = user).order_by('date').first()
            
            if appointment:
                # calculate the time remaining to the appointment
                current_datetime = datetime.datetime.now()
                appointment_datetime = datetime.datetime.combine(appointment.date, appointment.time)
                time_remaining = appointment_datetime - current_datetime
                days_remaining = time_remaining.days
                hours_remaining = time_remaining.seconds // 3600

                appointment.days_remaining = days_remaining
                appointment.hours_remaining = hours_remaining

            context = {
                'appointment': appointment,
            }
            return render(request, 'core/home.html', context)
        except Exception as e:
            messages.error(request, 'An error occurred while trying to get your upcoming appointment. Please try again later.')
        
        return render(request, 'core/home.html', context)

class Profile(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    
    def get(self, request):
        return render(request, 'profile/profile.html')

class UpdateProfileImage(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def redirect_profile(self):
        """Redirects user to the profile edit section."""
        return redirect(f"{reverse('profile')}#profile-edit")
    
    def get(self, request):
        return self.redirect_profile()

    def post(self, request):
        try:            
            profile = UserProfile.objects.get(user = request.user)

            if 'profile_picture' not in request.FILES or not request.FILES['profile_picture']:
                messages.error(request, 'You did not provide a profile picture. Please choose a file to upload.')
                return self.redirect_profile()
                
            image = request.FILES['profile_picture']

            if not profile.image.name == profile.image.field.default:
                profile.image.delete() # delete the old image if it was not the default image.
                
            profile.image = image        
            profile.save()
            messages.success(request, 'Profile picture updated successfully')
            return redirect('profile')
        
        # cant find the user profile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Trouble associating you with a profile. Please try')
            return self.redirect_profile()
        
        except Exception as e:
            messages.error(request, 'An error occurred while updating your profile picture. Please try again later')
            return self.redirect_profile() 

class UpdateProfileInfo(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        return self.redirect_profile()
    
    def redirect_profile(self): 
        """Redirects user to the profile edit section."""
        return redirect(f"{reverse('profile')}#profile-edit")
    
    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user = user)

            updated_bio = request.POST['bio']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
                
            if not first_name:
                messages.warning(request, 'Please provide your first name.')
                return self.redirect_profile()
            
            if not last_name:
                messages.warning(request, 'Please provide your last name.')
                return self.redirect_profile()
            
            if not username:
                messages.warning(request, 'Please provide your username.')
                return self.redirect_profile()
                
            if username == user.username and first_name == user.first_name and last_name == user.last_name and updated_bio == user_profile.bio:
                messages.info(request, 'No changes were made to your profile.')
                return self.redirect_profile()  
            
            if username != user.username and User.objects.filter(username = username).exists():
                messages.error(request, 'The username you provided is already taken. Please choose another one.')
                return self.redirect_profile()

           
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user_profile.bio = updated_bio

            user.save()
            user_profile.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('profile') # Return the use  to their profile.

        except UserProfile.DoesNotExist:
            messages.error(request, 'Trouble associating you with a profile. Please try again later.')
            return self.redirect_profile()
        except Exception as e:
            messages.error(request, f'An error occurred while updating your profile. Please try again later, {e}')
            return self.redirect_profile()
        
class UpdatePassword(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def redirect_profile(self):
        """Redirects user to the password edit section."""
        return redirect(f"{reverse('profile')}#password-edit")
    
    def get(self, request):
        return self.redirect_profile()
     
    def post(self, request):
        try:
            user = request.user
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if not current_password or not new_password or not confirm_password:
                messages.error(request, 'Please fill in all the fields.')
                return self.redirect_profile()

            if not user.check_password(current_password):
                messages.error(request, 'The old password you provided is incorrect.')
                return self.redirect_profile()
            
            if new_password != confirm_password:
                messages.error(request, 'The new password and confirm password do not match.')
                return self.redirect_profile()

            if new_password == current_password:
                messages.error(request, 'The new password cannot be the same as the old password.')
                return self.redirect_profile()

            if len(new_password) < 6:
                messages.error(request, 'The new password must be at least 6 characters long.')
                return self.redirect_profile()
            
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully')
            return redirect("profile")
        except Exception as e:
            messages.error(request, 'An error occurred while updating your password. Please try again later')
            return self.redirect_profile()

class DeleteProfileImage(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def redirect_profile(self):
        """Redirects user to the profile edit section."""
        return redirect(f"{reverse('profile')}#profile-edit")
    
    def get(self, request):
        return self.redirect_profile()

    def post(self, request):
        try: 
            profile = UserProfile.objects.get(user = request.user)

            if profile.image.name == profile.image.field.default:
                messages.error(request, "You don't have a profile picture to delete.")
                return self.redirect_profile()
            
            profile.image.delete()
            # set the image to the default image
            profile.image = profile.image.field.default
            profile.save()
            
            messages.success(request, 'Profile picture deleted successfully')
            return redirect('profile')
        
        except UserProfile.DoesNotExist:
            messages.error(request, 'Trouble associating you with a profile. Please try again later.')
            return self.redirect_profile()
        except Exception as e:
            messages.error(request, 'An error occurred while deleting your profile picture. Please try again later')
            return self.redirect_profile()

class ViewProfile(View):
    def get(self, request, username):
        try:
            # subject refers the user whose profile is being viewed
            subject = User.objects.get(username = username)

            context = {
                'subject': subject,
            }

            return render(request, 'profile/view_profile.html', context)
        except User.DoesNotExist:
            messages.error(request, "The user you are trying to view does not exist.")
            return redirect('home')
        except Exception as e:
            messages.error(request, "An error occurred while trying to view the profile. Please try again later.")
            return redirect('book_appointment')

