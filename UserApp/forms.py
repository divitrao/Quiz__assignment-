from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreation(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password1', 'password2']
        
        
class CustomUserChange(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)
    