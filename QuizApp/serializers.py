from rest_framework import serializers
from .models import Quiz, Question, Answer, Progress, Results

class QuizSerializers(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ( 'id','alloted_time','slug','quiz_description',)


class AnswerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id','options','check_answer_bool']


class ProgressSerializers(serializers.ModelSerializer):

    class Meta:
        model = Progress
        fields = ['minutes','seconds']

class QuestionOnlySerializer(serializers.ModelSerializer):
    answers = AnswerSerializers(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id','question','type','marks','answers',]


class QuestionSerializers(serializers.ModelSerializer):
    answers = AnswerSerializers(many = True, read_only = True)
    progress = serializers.SerializerMethodField(method_name='get_progress')

    class Meta:
        model = Question
        fields = ['id','question','type','marks','answers','progress',]
    
    def get_progress(self,obj):
        if self.context.get('first_question') is None:
            query = Progress.objects.filter(user = self.context.get('user'),
                                            subject = self.context.get('subject'),
                                            )
        else:
            query = Progress.objects.filter(user = self.context.get('user'),
                                            subject = self.context.get('subject'),
                                            question = self.context.get('first_question'))
        return(ProgressSerializers(query,many=True).data)

class ResultQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Results
        fields =  ['user_answer','correct_answer','question_text']

 


        