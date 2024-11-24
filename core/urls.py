from django.urls import path
from .views import Authenticated, Index, Profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('authenticated/', Authenticated.as_view(), name = 'authenticated'),
    path('profile/', Profile.as_view(), name = 'profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)