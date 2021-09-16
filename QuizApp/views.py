from django.db import models
from django.http import request
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .models import Quiz, Question, UserAnswer, CorrectAnswer
from .forms import AnswerForm
from django.urls import reverse, reverse_lazy
import uuid


class QuizzList(ListView):
    model = Quiz
    template_name = 'quizzList.html'
    context_object_name = 'quizlists'

    def get_queryset(self) :
        return Quiz.objects.all()


class PlayQuiz(FormView):
    form_class = AnswerForm
    template_name = 'game.html'

    

    def dispatch(self, request, *args, **kwargs):
        if request.POST:
            userChoosenOption = request.POST.get('textAnswer')
    
            # print('selected id dispatch ',userChoosenOption)
            if request.POST.get('textAnswer') is not None:
                mcq = True
                try:
                    uuid.UUID(userChoosenOption, version=4)
                except ValueError:
                    mcq= False
                
                print('MCQ is ', mcq)
                if mcq:
                    checkAnswer = CorrectAnswer.objects.filter(correctAnswerID = userChoosenOption, checkAnswerBool = 1)
                    find_question_id = CorrectAnswer.objects.filter(correctAnswerID = userChoosenOption).values('questionID')
                    question_id = find_question_id[0]['questionID']
                    question = Question.objects.get(questionID=question_id)
                    if len(checkAnswer)>0:
                        find_marks = (Question.objects.filter(questionID = question_id).values('marks'))
                        is_correct = True
                        marks = int(find_marks[0]['marks'])
                    else:
                        marks = 0
                        is_correct = False

                    currentScore = marks
                    userID = self.request.user.UserId
                    
                    obj = UserAnswer( currentScore=currentScore,
                                      UserId_id= userID,
                                      questionID= Question.objects.get(question = question) ,
                                      is_correct=is_correct
                                      )
                                               
                    obj.save()

                else:
                    # print('gdgdgdgdgdgdgdgd ',request.POST.get('get_id'))
                    userGussedAnswer = request.POST.get('textAnswer')
                    question_id = request.POST.get('get_id')
                    question = Question.objects.get(questionID=question_id)
                    answer_present = CorrectAnswer.objects.filter(questionID=question_id,answer__iexact=userGussedAnswer)
                    # print(answer_present,'ppppppppppppppppppppp')
                    if len(answer_present)>0:
                        # print('dddddddddddddddddddd')
                        find_marks = (Question.objects.filter(questionID = question_id).values('marks'))
                        is_correct = True
                        marks = int(find_marks[0]['marks'])
                    else:
                        marks = 0
                        is_correct = False

                    currentScore = marks
                    userID = self.request.user.UserId
                    
                    obj = UserAnswer( currentScore=currentScore,
                                      UserId_id= userID,
                                      questionID= Question.objects.get(question = question) ,
                                      is_correct=is_correct
                                      )
                                               
                    obj.save()

            else:
                question_id = request.POST.get('get_id')
                question = Question.objects.get(questionID=question_id)
                marks = 0
                is_correct = False
                userID = self.request.user.UserId
                obj = UserAnswer( currentScore=marks,
                                      UserId_id= userID,
                                      questionID= Question.objects.get(question = question) ,
                                      is_correct=is_correct
                                      )
                                               
                obj.save()

                
        print('222222222222222222222222')
        
        return super().dispatch(request, *args, **kwargs)

    # def post(self, request, *args: str, **kwargs) :
        
    #     return super().post(request, *args, **kwargs)

    def get_form(self,*args, **kwargs):
        self.slug = self.kwargs.get('slug')
        self.unanswered_question = UserAnswer.get_unanswered_question(self,self.request.user.UserId,Quiz.objects.get(category = self.slug).quizId)
        if self.unanswered_question is None:
            return render(request, 'progress.html')
        else:
            self.question = self.unanswered_question.first()
            # print('ggggggggggggggg',self.question)
            self.type = self.question.type
        return self.form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        
        return dict(kwargs,question=self.question,type=self.type)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewer_question'] = self.question.question
        question_set = Question.get_questions(self,Quiz.objects.get(category = self.slug).quizId)
        print(question_set)
        return context


    

    
    def form_valid(self, form):
        guess = form.cleaned_data['textAnswer']
        print('hhhhhhhhhhh',guess)
        return super().form_valid(form)

        
    def form_invalid(self, form) :
        print('selected id is from invalid ',self.request.POST.get('textAnswer'))
        return super().form_invalid(form)


    def get_success_url(self) :
        return reverse_lazy('QuizApp:playquiz', kwargs={'slug':self.slug})

  

    


