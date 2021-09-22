from django.db import models
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
    quizDescription = models.CharField(max_length=300)
    slug = models.SlugField(null=True, blank=True, max_length=100)
    alloted_time = models.IntegerField(default=5)
    category = models.CharField(max_length=100,choices=subjects,unique=True)

    def save(self, *args, **kwargs):
        value = self.category
        self.slug = slugify(value,allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.category

class Question(models.Model):

    question_type= [
        ("mcq","MCQ"),
        ("one_word","one_word")
    ]
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    type = models.CharField(max_length=30,choices=question_type)
    marks = models.IntegerField(default=0)
    question = models.CharField(max_length=1000)


    def __str__(self):
        return self.question

class Answer(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.CharField(max_length=100)
    checkAnswerBool = models.BooleanField(default=False)


    def __str__(self):
        return self.options