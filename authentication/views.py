from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
import json
from django.http import JsonResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile, Roles, Doctor
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.models import Group

validate_email = EmailValidator()


def send_activation_email(request, user, email, resend=False):
    try:
        # Send activation email
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        domain = get_current_site(request).domain
        link = reverse('activate_account', kwargs={'uidb64': uidb64, 'token': token})
        activate_url = f"{request.scheme}://{domain}{link}"
        if resend:
            email_subject = "New activation link." # include in the email subject if it is a new email while resending.
        else:
            email_subject = "Activate your account"
        email_body = f'Hello, {user.username},\n\nTo activate your account, click on the link below:\n\n{activate_url}'

        email_message = EmailMessage(email_subject, email_body, 'noreply@semycolon.com', [email])
        EmailThread(email_message).start()

        return True
    except Exception as e:
        messages.error(request, "An error occured sending the email")
        return False

    
# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        identifier = request.POST['usernameEmail'].strip()  # username or email.
        password = request.POST['password']

        context = {
            'username': identifier,
            }

        if not identifier or not password:
            messages.error(request, 'All fields are required. Please check and try again.')
            return render(request, 'authentication/login.html', context)
        
        try:
            if '@' in identifier:
                user = User.objects.get(email = identifier)
            else:
                user = User.objects.get(username = identifier)
          
        except User.DoesNotExist:
            messages.error(request, 'Invalid username/email or password. Please try again.')
            return render(request, 'authentication/login.html', context)

        if user is not None and not user.is_active:
            messages.error(request, "Your account has not been activated. Please check your email to activate your account, then try again.")
            return render(request, 'authentication/login.html', context)

        user = authenticate(request, username = user.username, password = password)
        if user is None:
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'authentication/login.html', context)
        
        try:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name.title()}')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred while logging in. Please try again {e}')
            return render(request, 'authentication/login.html', context)

# CLASS TO REGISTER THE USER.    
class Register(View):
    # validate the data.
    def validate_data(self, request, data):
        """Validates user data."""
        context = self.get_context(data)

        if not all([data['first_name'], data['last_name'], data['role'], data['username'], data['password'], data['confirm_password'], data['email']]):
            messages.error(request, "All fields are required.")
            return render(request, 'authentication/register.html', context)
        
        # Validate name fields
        if not data["first_name"].isalpha():
            messages.error(request, 'First name must contain letters only.')
            return render(request, 'authentication/register.html', context)
        if not data["last_name"].isalpha():
            messages.error(request, 'Last name must contain letters only.')
            return render(request, 'authentication/register.html', context)

        # Validate username
        if not data["username"].isalnum():
            messages.error(request, 'Username must contain letters and numbers only.')
            return render(request, 'authentication/register.html', context)
        if User.objects.filter(username=data["username"]).exists():
            user = User.objects.get(username=data["username"])
            
            if user.is_active:
                messages.error(request, 'Email already exists. Please log in instead.')
                return redirect('login')
            else:
                messages.error(request, "Account exists but is inactive. Please activate the account first.")
                request.session['email'] = user.email
                return redirect('confirm-email')

        # Validate email
        try:
            validate_email(data['email'])
        except ValidationError:
            messages.error(request, "'Email is invalid. Please enter a valid email.")
            return render(request, 'authentication/register.html', context)
        if User.objects.filter(email=data["email"]).exists():
            user = User.objects.get(email = data["email"])
            if user.is_active:
                messages.error(request, 'Email already exists. Please log in instead.')
                return redirect('login')
            else:
                messages.error(request, "Account exists but is inactive. Please activate the account first.")
                request.session['email'] = data["email"]
                return redirect('confirm-email')
        
        password = data['password'].strip()
        confirm_password = data['confirm_password']

         # Validate password
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'authentication/register.html', context)
        if len(password) < 6:
            messages.error(request, 'Password too short. Please use at least 6 characters.')
            return render(request, 'authentication/register.html', context)

         
        # Get the role object and validate
        try:
            role = Roles.objects.get(id=data['role'])
        except Roles.DoesNotExist:
            messages.error(request, 'Invalid role selected. Please select a valid role.')
            return render(request, 'authentication/register.html', context)

        # Validate additional fields for Doctor role
        if role.name == "Doctor":
            specialty = data.get('specialty')
            license_number = data.get('license_number')

            if not specialty:
                messages.error(request, "Specialty field is required for doctors.")
                return render(request, 'authentication/register.html', context)
            if not license_number:
                messages.error(request, "License number field is required for doctors.")
                return render(request, 'authentication/register.html', context)


        return True
    
    # get context for rendering pages to the frontend.
    def get_context(self, data):
        """Gets the context for rendering html pages."""
        roles = Roles.objects.all()

        context = {
            "roles": roles,
            "field_values": data
        }

        return context
    
    def get(self, request):
        """Renders page to the front end when get method is used."""
        roles = Roles.objects.all()
        return render(request, 'authentication/register.html', {'roles': roles})
        
    def post(self, request):
        """Registers the user when user's data is submitted from a form."""
        # get the form data
        data = request.POST

        username = data.get("username", "").strip()
        password = data.get('password', "").strip()
        email = data.get('email', "").strip()
        first_name = data.get('first_name', "").strip()
        last_name = data.get('last_name', "").strip()
        role_id = data.get('role', "").strip()

        validation_message = self.validate_data(request, data)
        
        if validation_message is not True:
            return validation_message

        context = self.get_context(data)
        
        # Get the role object and validate
        try:
            role = Roles.objects.get(id=role_id)
        except Roles.DoesNotExist:
            messages.error(request, 'Invalid role selected. Please select a valid role.')
            return render(request, 'authentication/register.html', context)

        # Create user and user profile
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            user.is_active = False  # Deactivate user account until activation
            user.save()

            if role.name == "Admin":
                user.is_staff = True
                user.save() # make the user a staff user if the  role is admin.

            user_profile = UserProfile(user=user, role=role)
            user_profile.save()

            # Create doctor if the role is Doctor
            if role.name == "Doctor":
                Doctor.objects.create(user_profile=user_profile, specialty=data["specialty"], license_number=data["license_number"])
                # add the use to doctors group
                group = Group.objects.get(name = "doctors")
                user.groups.add(group)

            # send the activation email to the user.
            if send_activation_email(request, user, email):
                request.session['email'] = email
                messages.success(request, "Your account was created successfully. Please check your email to activate your account.")
            return redirect('confirm-email')
        except Exception as e:
            user.delete()
            messages.error(request, f'An error occurred while creating your account. Please try again. {str(e)}')
            return render(request, 'authentication/register.html', context)

class ResendEmail(View):
    """Resends activation email."""
    def get(self, request):
        email = request.session.get('email', "undefined")
        return render(request, 'authentication/confirm_email.html', {"email": email})
    
    def post(self, request):
        email = request.POST.get('email').strip()
        user = User.objects.get(email=email)

        if not email:
            messages.error(request, "Email field is empty")
            return redirect('confirm-email')
        
        try:
            if send_activation_email(request, user, email, resend=True):
                messages.success(request, f"A new link was sent to {email}")
            return redirect('confirm-email')
            
        except Exception as e:
            messages.error(request, f"There was an error sending your new activation link. {e}")
            return redirect('confirm-email')



class ActivateAccount(View):
    """Uses the credential encoded in a link to activate the user's account."""
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)

            # check if the token has already been used to activate the account.
            if not token_generator.check_token(user, token):
                messages.error(request, 'Account has already been activated. Please login to continue.')
                return redirect('login')
            
            if user.is_active:
                messages.info(request, 'Account already activated. Please login to continue.')
                return redirect('login')
            
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully. Login to proceed.")
            return redirect('login')
        except Exception as e:
            messages.error(request, 'An error occurred while activating your account. Please try again.')
            return redirect('register')
        
class ValidateName(View):
    """Ensure the name is alphanumeric with no special characters."""
    def post(self, request):
        data = json.loads(request.body)
        name = data['name'].strip()

        # ensure the name contains letters only
        if not name.isalpha():
            return JsonResponse({'name_error': 'Name must contain letters only'}, status=400)
        
        return JsonResponse({'name_valid': True})

        

class ValidateUsername(View):
    """Ensure username is unique and in the correct format. Accessible in real time as user keys in the username in registration form."""
    def post(self, request):
        data = json.loads(request.body)
        username = data['username'].strip()

        # ensure username contains alphanumeric characters only.
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username must contain letters and numbers only'}, status = 400)
        
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'Username taken. Choose another one.'}, status=409)
        return JsonResponse({'username_valid': True})

class ValidateEmail(View):
    """Ensures the email is unique and valid. Used in real time as user key's in the email."""
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()

            if User.objects.filter(email = email).exists():
                return JsonResponse({'email_error': 'Email already exists. Use another email.'}, status=400)
          
            validate_email(email)
            return  JsonResponse({'email_valid': True})
        except ValidationError:
            return JsonResponse({'email_error': 'Email is invalid. Please enter a valid email.'}, status=409)
        except json.JSONDecodeError as e:
            return JsonResponse({"email_error": "Error decoding email into json."}, status = 400)
        
       

class Logout(View):
    """Log out the user."""
    def post(self, request):
        try:
            logout(request)
            messages.success(request, 'You have been logged out successfully.')
            return redirect('index')
        except Exception as e:
            messages.error(request, 'An error occurred while logging out. Please try again.')
            return redirect('home')

class ResetPassword(View):
    """Send a password reset link to the user."""
    def get(self, request):
        return render(request, 'authentication/reset_password.html')
    
    def post(self, request):
        try:
            email = request.POST['email']

            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Invalid Email. Please enter a valid email.")
                return redirect('reset-password')
            
            user = User.objects.filter(email=email).first()
            if not user:
                messages.error(request, 'A user with the email provided does not exist. Please check and try again.')
                return redirect('reset-password')

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            domain = get_current_site(request).domain
            link = reverse('set-new-password', kwargs={'uidb64': uidb64, 'token': token})

            reset_url = f"{request.scheme}://{domain}{link}"
            email_subject = "Password Reset"
            email_body = f'Hello, {user.username}, \n\nTo reset your password, click on the link below.\n\n{reset_url}'

            email = EmailMessage(
                email_subject,
                email_body, 
                "noreply@semycolon.com",
                [email],
            )
                
                
            EmailThread(email).start()
            messages.success(request, 'Password reset link has been sent to your email. Please check your email to reset your password.')
            return redirect('reset-password')
        except Exception as e:
            messages.error(request, f'An error occurred while sending the email. Please try again. {e}')
            return render(request, 'authentication/reset_password.html')
        
class SetNewPassword(View):
    """Allows a user to change their password."""
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        return render(request, 'authentication/set_new_password.html', context)

    def post(self, request,  uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if len (password) < 6:
            messages.error(request, 'Password too short. Please use at least 6 characters.')
            return render(request, 'authentication/set_new_password.html', context)

        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'authentication/set_new_password.html', context)
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, 'The link is invalid. Please request a new link.')
                return redirect('reset-password')
            
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Password reset successful. You can now login with your new password.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'An error occurred while resetting your password. Please try again.')
            return render(request, 'authentication/set_new_password.html', context)


class EmailThread(threading.Thread):
    # speed up the sending of the email and response back to the user.
    
    def __init__(self, email):
       self.email = email
       threading.Thread.__init__(self)
       
    def run(self):
        self.email.send(fail_silently = False)