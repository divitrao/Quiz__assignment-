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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_description = models.CharField(max_length=300)
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
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    type = models.CharField(max_length=30,choices=question_type)
    marks = models.IntegerField(default=0)
    question = models.CharField(max_length=1000)

    def get_questions(self,quiz_id):
        question_set = Question.objects.filter(quiz = quiz_id)
        return question_set

    def __str__(self):
        return self.question


class CorrectAnswer(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    check_answer_bool = models.BooleanField(default=False)

    
    def get_answer_list(self, questionID):
        options = CorrectAnswer.objects.filter(question=questionID).values_list('id','answer')
        return options

    def __str__(self):
        return self.answer


class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user= models.ForeignKey(CustomUser,on_delete=models.PROTECT)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=100, blank=True, verbose_name="")
    is_correct  = models.BooleanField(default=False)
    current_score = models.IntegerField(default=0) 

    def get_unanswered_question(self, user_id,quiz):
        answered_list = UserAnswer.objects.filter(user = user_id).values_list('question')
        unanswered_list = Question.objects.filter(quiz=quiz).exclude(question__in=answered_list)
        if len(unanswered_list) == 0:
            return None 
        else:
            return unanswered_list


    def __str__(self):
        return self.question.question

class Progress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    minutes = models.IntegerField(default=1)
    seconds = models.IntegerField(default=60)
    subject = models.CharField(max_length=20)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.PROTECT)

    def __str__(self):
        return self.subject + ' '+ self.user.username


   
