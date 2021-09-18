from django.contrib import admin
from .models import Quiz, Question, CorrectAnswer, UserAnswer, Progress
# Register your models here.


class OptionInline(admin.TabularInline):
    model = CorrectAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline,]
    list_display = ['quizId', 'type', 'marks', 'question'] 



myModel = [Quiz,UserAnswer]

admin.site.register(myModel)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Progress)

