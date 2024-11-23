from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
import json
from django.http import JsonResponse
from validate_email import validate_email

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
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        role = request.POST['role']

        user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, role = role)
        user.set_password(password)
        user.save()
        
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
