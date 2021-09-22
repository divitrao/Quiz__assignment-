from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import QuizSerializer
from .models import Quiz
# Create your views here.

class ListQuiz(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
