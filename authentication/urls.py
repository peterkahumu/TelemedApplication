from django.urls import path
from .views import Register, Login, ValidateEmail, ValidateUsername, ValidateName, Logout
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('register', Register.as_view(), name = 'register'),
    path('validate_name', csrf_exempt(ValidateName.as_view()), name = 'validate-name'),
    path('validate_email', csrf_exempt(ValidateEmail.as_view()), name='validate-email'),
    path('validate_username', csrf_exempt(ValidateUsername.as_view()), name='validate-username'),
    path('logout', Logout.as_view(), name = 'logout'),
    
]