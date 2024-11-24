from django.urls import path
from .views import Authenticated, Index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('authenticated/', Authenticated.as_view(), name = 'authenticated'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)