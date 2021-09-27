from django.urls import path 
from .views import PlayQuiz,  Result, UpdateTime, QuizList

app_name = 'QuizApp'

urlpatterns = [
                path('quizlist/',QuizList.as_view(),name='quizlist'),
                path('<slug>/',PlayQuiz.as_view(),name='playquiz'),
                path('<result>/<slugs>/', Result.as_view(), name='result'),
                path('timeupdate/',UpdateTime.as_view(),name='timeupdates'),]

