from django.urls import path
from .views import QuizzList 
from .views import PlayQuiz


app_name = 'QuizApp'

urlpatterns = [

path('quizlist',QuizzList.as_view(),name='quizlist'),
path('<slug:slug>/',PlayQuiz.as_view(),name='playquiz')

]