from rest_framework import serializers
from .models import Quiz, Question, Answer

class QuizSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ( 'id','alloted_time','category',)


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id','options','checkAnswerBool']

class QuestionSerializers(serializers.ModelSerializer):
    answers = AnswerSerializers(many = True, read_only = True)
    class Meta:
        model = Question
        fields = ['id','question','type','marks','answers',]