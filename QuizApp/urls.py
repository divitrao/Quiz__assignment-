from django.urls import path
from .views import ListQuiz, ListQuestions

urlpatterns = [ 
    path('',ListQuiz.as_view(), name='listQuiz'),
    path('<slug:slug>',ListQuestions.as_view(),name='listQuestions')
]