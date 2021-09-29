from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomePageView, SignUpView

app_name = 'UserApp'

urlpatterns = [ 
    path('', HomePageView.as_view(), name='home'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name ='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name ='logout.html'), name='logout')
]