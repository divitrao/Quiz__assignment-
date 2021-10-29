from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomePageView, SignUpView, LoginView, LogoutView

app_name = 'UserApp'

urlpatterns = [ 
    path('', HomePageView.as_view(), name='home'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]