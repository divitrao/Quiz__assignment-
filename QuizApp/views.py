from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Quiz, Question, Results, UserAnswer
from .serializers import QuizSerializers, QuestionSerializers, ResultQuestionSerializer, QuestionOnlySerializer 
from rest_framework.response import Response
from django.views.generic import TemplateView

class ListQuiz(ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializers


class ListQuestions(APIView):
    def get(self, request, format=None, **kwargs):
        user_answered_question = UserAnswer.objects.filter(user=request.user.id , 
                                                           question__quiz__category = kwargs['slug'])\
                                                            .values_list('question')
        user_unanswered_questions = Question.objects.filter(quiz__category=kwargs['slug'])\
                                                            .exclude(id__in = user_answered_question)
        
        if len(user_unanswered_questions) > 0:

            serializer = QuestionSerializers(user_unanswered_questions, 
                                             many = True , 
                                             context = {'user':request.user.id,
                                                        'subject':kwargs['slug'],
                                                        'first_question':user_unanswered_questions[:1][0].id})
        else:
            questions = Question.objects.filter(quiz__category = kwargs['slug'])
            serializer = QuestionOnlySerializer(questions, many = True ,)
        
        return Response(serializer.data)

class QuizListView(TemplateView):
    template_name = 'quiz_subject_list.html'


class ResultViewApi(APIView):
    def get(self,request,format=None, **kwargs):
        test_result = Results.objects.filter(user = request.user.id ,
                                             exam_number=kwargs['exam_number'] , 
                                             question__quiz__category = kwargs['subject'])
        serializer = ResultQuestionSerializer(test_result, many=True)
        return Response(serializer.data)
    

