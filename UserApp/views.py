
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from rest_framework import serializers
from rest_framework import response
from rest_framework.response import Response
from .forms import CustomUserCreation
from django.urls import reverse_lazy
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth.models import auth
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.utils.decorators import method_decorator


class HomePageView(TemplateView):
    template_name = 'home.html'


class SignUpView(APIView):
    def post(self,request):
        # print(request.data,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

# @method_decorator(csrf_exempt)
class LoginView(APIView):
    @csrf_exempt
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        print(request.data)

        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise AuthenticationFailed('user not found')
        else:
            auth.login(request,user)

        payload = {
            'id':str(user.id),
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm='HS256')

        response  = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'jwt':token
        }

        return response


class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'loggged out succesfully'
        }

        return response
