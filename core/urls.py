from django.urls import path
from .views import Authenticated, Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('authenticated/', Authenticated.as_view(), name = 'authenticated'),
]