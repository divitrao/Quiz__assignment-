from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Quiz, Question, Answer
from .serializers import QuizSerializers, QuestionSerializers
from rest_framework.response import Response

class ListQuiz(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializers

class ListQuestions(APIView):
    def get(self, request, format=None, **kwargs):
        questions = Question.objects.filter(quiz__category=kwargs['slug'])
        serializer = QuestionSerializers(questions, many = True)
        return Response(serializer.data)
