from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('home/', Home.as_view(), name = 'home'),
    path('profile/', Profile.as_view(), name = 'profile'),
    path('update-profile-image/', UpdateProfileImage.as_view(), name = 'update_profile_image'),
    path('update-profile-info/', UpdateProfileInfo.as_view(), name = 'update_profile_info'),
    path('update-password/', UpdatePassword.as_view(), name = 'update_password'),
    path('delete-profile-image/', DeleteProfileImage.as_view(), name = 'delete_profile_image'),
    path('view_profile/<username>/', ViewProfile.as_view(), name = 'view_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)