from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        return render(request, 'authentication/authenticated.html')
    

class Register(View):
    def get(self, request):

        return render(request, 'authentication/register.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        email = request.POST['email']
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        role = request.POST['role']

        context = {
            'field_values': {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            },
            'selected_role': role
        }

        if not first_name or not last_name or not username or not email or not password or not confirm_password or not role:
            messages.error(request, 'All fields are required. Please cross-check and provide the required information.')
            return render(request, 'authentication/register.html', context)

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'authentication/register.html', context)
           
        if len(password) < 6:
            messages.error(request, 'Password too short. Please use at least 6 characters')
            return render(request, 'authentication/register.html', context)
        
        try:
            user = User.objects.create_user(username = username, email = email, password = password, first_name = first_name, last_name = last_name)
            user_profile = UserProfile(user = user, role = role)
            user_profile.save()

            messages.success(request, f'{username}, your account was created successfully')
            return redirect ('authenticated')
        except Exception as e:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return render(request, 'authentication/register.html', context)
        
        messages.success(request, 'Account created successfully')
        return redirect('authenticated')


class ValidateName(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data['name'].strip()

        # ensure the name contains letters only
        if not name.isalpha():
            return JsonResponse({'name_error': 'Name must contain letters only'}, status=400)
        
        return JsonResponse({'name_valid': True})

        

class ValidateUsername(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username'].strip()

        # ensure username contains alphanumeric characters only.
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username must contain letters and numbers only'}, status = 400)
        
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'Username already exists. Use another username.'}, status=400)
        return JsonResponse({'username_valid': True})

class ValidateEmail(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email'].strip()
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error': 'Email already exists. Use another email.'}, status=400)
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid. Please enter a valid email.'}, status=400)
        
        return JsonResponse({'email_valid': True})

