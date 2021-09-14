from django.db import models
from UserApp.models import CustomUser
import uuid


class Quiz(models.Model):
    subjects =[

        ("history","History"),
        ("geography","Geography"),
        ("science","science"),
        ("maths","Maths")
        ]
    quizId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DurationField(blank=True)
    quizDescription = models.CharField(max_length=300)
    category = models.CharField(max_length=100,choices=subjects)

    def __str__(self):
        return self.category


class Question(models.Model):

    question_type= [
        ("mcq","MCQ"),
        ("one_word","one_word")
    ]
    questionID= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    type = models.CharField(max_length=30,choices=question_type)
    marks = models.IntegerField(default=0)
    question = models.CharField(max_length=1000)

    def __str__(self):
        return self.question


class CorrectAnswer(models.Model):
    correctAnswerID = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    checkAnswerBool = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class UserAnswer(models.Model):
    answerId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UserId= models.ForeignKey(CustomUser,on_delete=models.PROTECT)
    questionID = models.ForeignKey(Question,on_delete=models.CASCADE)
    textAnswer = models.CharField(max_length=100, blank=True)
    remainingTime = models.DurationField(blank=True)
    correctAnswerID = models.ForeignKey(CorrectAnswer,on_delete=models.CASCADE)
    currentScore = models.IntegerField(default=0) # doubtfull as per Rahul 
    examCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.text_ans
   
