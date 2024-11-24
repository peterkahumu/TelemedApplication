from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UserProfile
from django.contrib import messages

# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, 'core/index.html')


class Authenticated(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    
    def get(self, request):
        return render(request, 'core/authenticated.html')

class Profile(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    
    def get(self, request):
        return render(request, 'core/profile.html')

class UpdateProfileImage(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'core/profile.html')

    def post(self, request):
        try:            
            profile = UserProfile.objects.get(user = request.user)

            if 'profile_picture' not in request.FILES or not request.FILES['profile_picture']:
                messages.error(request, 'You did not provide a profile picture. Please choose a file to upload.')
                return redirect('profile')    
                
            image = request.FILES['profile_picture']

            # delete the existing image permanently and save the new one.
            profile.image.delete()
            profile.image = image        
            profile.save()
            messages.success(request, 'Profile picture updated successfully')
            return redirect('profile')
        # cant find the user profile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Trouble associating you with a profile. Please try')
            return redirect('profile')
        
        except Exception as e:
            messages.error(request, 'An error occurred while updating your profile picture. Please try again, ' + str(e))
            return redirect('profile')