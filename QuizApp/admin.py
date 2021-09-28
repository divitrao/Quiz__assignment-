from django.contrib import admin
from .models import Quiz, Question, Answer, UserAnswer, Progress, Results



@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['category', 'alloted_time']

class AnswerAdmin(admin.TabularInline):
    model = Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'type', 'marks', 'quiz']
    inlines = [AnswerAdmin]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [ 
        'options', 'question',]
    

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = [ 'user' , 'question' , 'user_answer']
    
          

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    pass

@admin.register(Results)
class ResultAdmin(admin.ModelAdmin):
    pass