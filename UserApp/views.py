from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
# Create your views here.
class home_page(TemplateView):
    template_name = 'home.html'


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/account/two_factor/setup/' #reverse_lazy('login')
    template_name = 'registration/signup.html'