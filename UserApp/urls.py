from django.urls import  path 
from .views import home_page 
from .views import SignupView



urlpatterns = [
    path('',home_page.as_view(),name='home'),
    path('signup/',SignupView.as_view(),name='signup'),
]