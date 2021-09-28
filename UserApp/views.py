
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import CustomUserCreation
from django.urls import reverse_lazy


class HomePageView(TemplateView):
    template_name = 'home.html'


class SignUpView(FormView):
    form_class = CustomUserCreation
    template_name = 'signup.html'
    success_url = reverse_lazy('two_factor:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)