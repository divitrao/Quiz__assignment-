from django.contrib import admin
from .models import Quiz, Answer, Question
# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass

class AnswerAdmin(admin.TabularInline):
    model = Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin,]
    list_display = ['question','type','marks','quizId']



