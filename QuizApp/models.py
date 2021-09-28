from django.db import models
from UserApp.models import CustomUser
import uuid
from django.utils.text import slugify
class Quiz(models.Model):
    subjects =[

        ("history", "History"),
        ("geography", "Geography"),
        ("science", "science"),
        ("maths", "Maths"),
        ("entertainment", "Entertainment"),
        ('vehicle', 'vehicle')
        ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_description = models.CharField(max_length=300)
    slug = models.SlugField(null=True, blank=True, max_length=100)
    alloted_time = models.IntegerField(default=5)
    category = models.CharField(max_length=100, choices=subjects, unique=True)

    def save(self, *args, **kwargs):
        value = self.category
        self.slug = slugify(value, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.category

class Question(models.Model):

    question_type= [
        ("mcq","MCQ"),
        ("one_word","one_word")
    ]
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=30, choices=question_type)
    marks = models.IntegerField(default=0)
    question = models.CharField(max_length=1000)


    def __str__(self):
        return self.question

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    options = models.CharField(max_length=100)
    check_answer_bool = models.BooleanField(default=False)


    def __str__(self):
        return self.options


class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=100, blank=True, verbose_name="")
    is_correct  = models.BooleanField(default=False)
    current_score = models.IntegerField(default=0)  

    


    def __str__(self):
        return self.question.question

class Progress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    minutes = models.IntegerField(default=1)
    seconds = models.IntegerField(default=60)
    subject = models.CharField(max_length=20)
    question = models.ForeignKey(Question,on_delete=models.CASCADE, related_name='progress')
    user = models.ForeignKey(CustomUser,on_delete=models.PROTECT, related_name='user_progress')

    def __str__(self):
        return self.subject + ' '+ self.user.username


class Results(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_for_result')
    user_answer = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)
    marks_achieved = models.IntegerField()
    exam_number = models.IntegerField()
    question_text = models.CharField(max_length=1000)