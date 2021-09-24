from django.db import models
from django.db.models.deletion import CASCADE
from UserApp.models import CustomUser
import uuid
from django.utils.text import slugify
class Quiz(models.Model):
    subjects =[

        ("history","History"),
        ("geography","Geography"),
        ("science","science"),
        ("maths","Maths"),
        ("entertainment","Entertainment"),
        ('vehicle','vehicle')
        ]
    quizId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quizDescription = models.CharField(max_length=300)
    slug = models.SlugField(null=True, blank=True, max_length=100)
    alloted_time = models.IntegerField(default=5)
    category = models.CharField(max_length=100,choices=subjects,unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category,allow_unicode=True)
        return super().save(*args, **kwargs)

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

    def get_questions(self,quiz_id):
        question_set = Question.objects.filter(quizId = quiz_id)
        return question_set

    def __str__(self):
        return self.question


class CorrectAnswer(models.Model):
    correctAnswerID = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    checkAnswerBool = models.BooleanField(default=False)

    
    def get_answer_list(self, questionID):
        options = CorrectAnswer.objects.filter(questionID=questionID).values_list('correctAnswerID','answer')
        return options

    def __str__(self):
        return self.answer


class UserAnswer(models.Model):
    answerId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UserId= models.ForeignKey(CustomUser,on_delete=models.PROTECT)
    questionID = models.ForeignKey(Question,on_delete=models.CASCADE)
    textAnswer = models.CharField(max_length=100, blank=True, verbose_name="")
    is_correct  = models.BooleanField(default=False)
    currentScore = models.IntegerField(default=0) # doubtfull as per Rahul 

    def get_unanswered_question(self, user_id,quiz):
        answered_list = UserAnswer.objects.filter(UserId = user_id).values_list('questionID')
        unanswered_list = Question.objects.filter(quizId=quiz).exclude(questionID__in=answered_list)
        if len(unanswered_list) == 0:
            return None 
        else:
            return unanswered_list


    def __str__(self):
        return self.questionID.question

class Progress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    minutes = models.IntegerField(default=1)
    seconds = models.IntegerField(default=60)
    subject = models.CharField(max_length=20)
    questionID = models.ForeignKey(Question,on_delete=models.CASCADE)
    UserId = models.ForeignKey(CustomUser,on_delete=models.PROTECT)

    def __str__(self):
        return self.subject + ' '+ self.UserId.username


   
