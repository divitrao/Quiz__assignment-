from django.urls import path
from .views import ListQuiz

urlpatterns = [ 

    path('',ListQuiz.as_view(),name='listquiz')
]