from django.contrib import admin
from .models import Quiz, Question, Answer



@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['category','alloted_time']

class AnswerAdmin(admin.TabularInline):
    model = Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question','type','marks','quiz']
    inlines = [AnswerAdmin]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [ 
        'options','checkAnswerBool','question',
    ]

