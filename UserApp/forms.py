from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        models = get_user_model()
        fields = ('email','username',)
        

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=75, required=True)
    class Meta:
        model = get_user_model()
        fields = ('email','username')
        # def __init__(self, *args, **kwargs):
        #     super(Customer_creator,self).__init__(*args,**kwargs)
        #     self.fields['email'].required = True

