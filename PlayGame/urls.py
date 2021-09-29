from django.urls import path
from .views import QuizListView, GameView, ResultView, UpdateToDatabase, UpdateTime

app_name = 'PlayGame'

urlpatterns = [ 
    path('updatetime/', UpdateTime.as_view(), name = 'updatetime'),
    path('update/', UpdateToDatabase.as_view(), name='update'),
    path('quizlist/', QuizListView.as_view(), name = 'quizlist'), #user view 
    path('start/', GameView.as_view(),name='gameview'),
    path('result/<str:slugs>/<str:exam_number>/', ResultView.as_view(), name='result')
    
]