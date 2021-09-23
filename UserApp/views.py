from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm


class HomePage(TemplateView):
    template_name = 'home.html'


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/account/two_factor/setup/' 
    template_name = 'registration/signup.html'