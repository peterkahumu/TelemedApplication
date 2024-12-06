from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UserProfile, User
from django.contrib import messages

# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class Home(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    
    def get(self, request):
        return render(request, 'core/home.html')

class Profile(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    
    def get(self, request):
        return render(request, 'profile/profile.html')

class UpdateProfileImage(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'profile/profile.html')

    def post(self, request):
        try:            
            profile = UserProfile.objects.get(user = request.user)

            if 'profile_picture' not in request.FILES or not request.FILES['profile_picture']:
                messages.error(request, 'You did not provide a profile picture. Please choose a file to upload.')
                return redirect('profile')    
                
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
            return redirect('profile')
        
        except Exception as e:
            messages.error(request, 'An error occurred while updating your profile picture. Please try again later')
            return redirect('profile')

class UpdateProfileInfo(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        return redirect('profile')
    
    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user = user)

            updated_bio = request.POST['bio']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']

            if username == user.username and first_name == user.first_name and last_name == user.last_name and updated_bio == user_profile.bio:
                messages.info(request, 'No changes were made to your profile')
                return redirect('profile')
            
            if username != user.username and User.objects.filter(username = username).exists():
                messages.error(request, 'The username you provided is already taken. Please choose another one.')
                return redirect('profile')

           
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user_profile.bio = updated_bio
            user.save()
            user_profile.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        
            
        except UserProfile.DoesNotExist:
            messages.error(request, 'Trouble associating you with a profile. Please try again later.')
            return redirect('profile')
        except Exception as e:
            messages.error(request, 'An error occurred while updating your profile. Please try again later')
            return redirect('profile')