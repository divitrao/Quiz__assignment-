from django.urls import path
from .views import ListQuiz, ListQuestions, ResultViewApi

app_name = 'QuizApp'

urlpatterns = [ 
    path('<subject>/<exam_number>/', ResultViewApi.as_view(), name='resultviewapi'),
    path('', ListQuiz.as_view(), name='quiz'), #API view 
    path('<slug:slug>/', ListQuestions.as_view(), name='listQuestions'),
    
    
]