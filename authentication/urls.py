from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name = 'register'),
    path('activate_account/<uidb64>/<token>', ActivateAccount.as_view(), name = 'activate_account'),
    path('validate_name', csrf_exempt(ValidateName.as_view()), name = 'validate-name'),
    path('validate_email', csrf_exempt(ValidateEmail.as_view()), name='validate-email'),
    path('validate_username', csrf_exempt(ValidateUsername.as_view()), name='validate-username'),
    path('logout', Logout.as_view(), name = 'logout'),
    path('reset_password', ResetPassword.as_view(), name = 'reset-password'),
    path('set_new_password/<uidb64>/<token>', SetNewPassword.as_view(), name = 'set-new-password'),
    path('confirm_email', ResendEmail.as_view(),  name='confirm-email')
    
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)