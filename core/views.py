from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UserProfile, User
from django.contrib import messages
from django.urls import reverse

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
        return redirect(f"{reverse('profile')}#profile-edit")

    def post(self, request):
        try:            
            profile = UserProfile.objects.get(user = request.user)

            if 'profile_picture' not in request.FILES or not request.FILES['profile_picture']:
                messages.error(request, 'You did not provide a profile picture. Please choose a file to upload.')
                return redirect(f"{reverse('profile')}#profile-edit") # redirect to the profile page with the edit section open.
                
            image = request.FILES['profile_picture']

            if not profile.image.name == profile.image.field.default:
                profile.image.delete() # delete the old image if it was not the default image.
                
            profile.image = image        
            profile.save()
            messages.success(request, 'Profile picture updated successfully')
            return redirect(f"{reverse('profile')}#profile-edit")
        
        # cant find the user profile
        except UserProfile.DoesNotExist:
            messages.error(request, 'Trouble associating you with a profile. Please try')
            return redirect(f"{reverse('profile')}#profile-edit")
        
        except Exception as e:
            messages.error(request, 'An error occurred while updating your profile picture. Please try again later')
            return redirect(f"{reverse('profile')}#profile-edit") 

class UpdateProfileInfo(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        return redirect(f"{reverse('profile')}#profile-edit")
    
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
                return redirect(f"{reverse('profile')}#profile-edit")
            if username != user.username and User.objects.filter(username = username).exists():
                messages.error(request, 'The username you provided is already taken. Please choose another one.')
                return redirect(f"{reverse('profile')}#profile-edit")

           
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user_profile.bio = updated_bio
            user.save()
            user_profile.save()

            messages.success(request, 'Profile updated successfully')
            return redirect(f"{reverse('profile')}#profile-edit")
        
            
        except UserProfile.DoesNotExist:
            messages.error(request, 'Trouble associating you with a profile. Please try again later.')
            return redirect(f"{reverse('profile')}#profile-edit")
        except Exception as e:
            messages.error(request, 'An error occurred while updating your profile. Please try again later')
            return redirect(f"{reverse('profile')}#profile-edit")
        
class UpdatePassword(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        return redirect(f"{reverse('profile')}#password-edit")
    
    
    def post(self, request):
        try:
            user = request.user
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if not current_password or not new_password or not confirm_password:
                messages.error(request, 'Please fill in all the fields.')
                return redirect(f"{reverse('profile')}#password-edit")

            if not user.check_password(current_password):
                messages.error(request, 'The old password you provided is incorrect.')
                return redirect(f"{reverse('profile')}#password-edit")
            
            if new_password != confirm_password:
                messages.error(request, 'The new password and confirm password do not match.')
                return redirect(f"{reverse('profile')}#password-edit")

            if new_password == current_password:
                messages.error(request, 'The new password cannot be the same as the old password.')
                return redirect(f"{reverse('profile')}#password-edit")

            if len(new_password) < 6:
                messages.error(request, 'The new password must be at least 6 characters long.')
                return redirect(f"{reverse('profile')}#password-edit")
            
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully')
            return redirect(f"profile")
        except Exception as e:
            messages.error(request, 'An error occurred while updating your password. Please try again later')
            return redirect(f"{reverse('profile')}#password-edit")

class DeleteProfileImage(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        return redirect(f"{reverse('profile')}#profile-edit")

    def post(self, request):
        try: 
            profile = UserProfile.objects.get(user = request.user)

            if profile.image.name == profile.image.field.default:
                messages.error(request, "You don't have a profile picture to delete.")
                return redirect(f"{reverse('profile')}#profile-edit")
            
            profile.image.delete()
            # set the image to the default image
            profile.image = profile.image.field.default
            profile.save()
            
            messages.success(request, 'Profile picture deleted successfully')
            return redirect(f"{reverse('profile')}#profile-edit")
        except UserProfile.DoesNotExist:
            messages.error(request, 'Trouble associating you with a profile. Please try again later.')
            return redirect(f"{reverse('profile')}#profile-edit")
        except Exception as e:
            messages.error(request, 'An error occurred while deleting your profile picture. Please try again later')
            return redirect(f"{reverse('profile')}#profile-edit")