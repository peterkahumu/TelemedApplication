from django.urls import path
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)