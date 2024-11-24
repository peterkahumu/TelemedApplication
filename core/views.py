from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, 'core/index.html')


class Authenticated(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    
    def get(self, request):
        return render(request, 'core/authenticated.html')

class Profile(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    
    def get(self, request):
        return render(request, 'core/profile.html')

