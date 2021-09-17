from django.db import models
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .models import Quiz, Question, UserAnswer, CorrectAnswer
from .forms import AnswerForm #AnswerUSerForm
from django.urls import  reverse_lazy
import uuid
from django.db.models import Sum


class QuizzList(ListView):
    model = Quiz
    template_name = 'quizzList.html'
    context_object_name = 'quizlists'

    def get_queryset(self) :
        return Quiz.objects.all()


class PlayQuiz(FormView):
    form_class = AnswerForm
    template_name = 'game.html'
    question_and_type = []
    

    def dispatch(self, request, *args, **kwargs):
        self.slug = self.kwargs.get('slug')
        quiz = get_object_or_404(Quiz,category = self.slug).quizId
        if UserAnswer.get_unanswered_question(user_id=self.request.user.UserId,quiz=quiz) == None:
            return redirect('QuizApp:result', result='result',slugs=self.slug)
        
        return super().dispatch(request, *args, **kwargs)

 

    def get_form(self,*args, **kwargs):
        if self.request.method == 'GET':
            self.question_and_type.clear()
            self.unanswered_question = UserAnswer.get_unanswered_question(self.request.user.UserId,
                                                                          Quiz.objects.get(category = self.slug).quizId)
            if self.unanswered_question is None:
                return render(self.request, 'progress.html')
            self.question = self.unanswered_question.first()
            self.type = self.question.type
            self.question_and_type.extend([self.question, self.type])
            return self.form_class(**self.get_form_kwargs())
        else :
            form = AnswerForm(question = self.question_and_type[0],
                              type = self.question_and_type[1], 
                              data = self.request.POST)
            return form

    def get_form_kwargs(self):
        if self.request.method == 'GET' :
            kwargs =  super().get_form_kwargs()
            return dict(kwargs,question=self.question,type=self.type)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewer_question'] = self.question_and_type[0]
        return context


    

    
    def form_valid(self, form):
        quiz = get_object_or_404(Quiz,category = self.slug).quizId
        user = self.request.user.UserId
        userChoosenOption = self.request.POST.get('textAnswer')
        if userChoosenOption is not None:
            mcq = True
            try:
                uuid.UUID(userChoosenOption, version=4)
            except ValueError:
                mcq= False
            if mcq:

                checkAnswer = CorrectAnswer.objects.get(correctAnswerID = userChoosenOption).checkAnswerBool
                question_id = CorrectAnswer.objects.get(correctAnswerID = userChoosenOption).questionID_id # questionID_id is name of column in database
                question = Question.objects.get(questionID=question_id)
                if checkAnswer==True:
                        marks = Question.objects.get(questionID = question_id).marks
                        is_correct = True
                else:
                        marks = 0
                        is_correct = False

                currentScore = marks
                userID = user
                choosed_answer = CorrectAnswer.objects.get(correctAnswerID = userChoosenOption).answer
                UserAnswer.objects.create(      currentScore=currentScore,
                                                        textAnswer = choosed_answer,
                                                        UserId_id= userID,
                                                        questionID= Question.objects.get(question = question) ,
                                                        is_correct=is_correct
                                                    )
                                                    
                            

            else:
                            
                        userGussedAnswer = self.request.POST.get('textAnswer')
                        question_id =  self.question_and_type[0].questionID
                        question = Question.objects.get(questionID=question_id)
                        answer_present = CorrectAnswer.objects.get(questionID=question_id).answer
                        if answer_present.strip().lower() == userGussedAnswer.strip().lower():
                            
                            marks= Question.objects.get(questionID = question_id).marks
                            is_correct = True
                        else:
                            marks = 0
                            is_correct = False
                        currentScore = marks
                        userID = user
                        UserAnswer.objects.create(  currentScore=currentScore,
                                                        textAnswer = userGussedAnswer,
                                                        UserId_id= userID,
                                                        questionID= Question.objects.get(question = question) ,
                                                        is_correct=is_correct
                                                    )
                                                    
                            

        else:
                        question_id = self.question_and_type[0].questionID
                        question = Question.objects.get(questionID=question_id)
                        marks = 0
                        is_correct = False
                        userID = user
                        UserAnswer.objects.create(  currentScore=marks,
                                                    textAnswer = 'Not Attempted',
                                                    UserId_id= userID,
                                                    questionID= Question.objects.get(question = question) ,
                                                    is_correct=is_correct
                                                )
        return super().form_valid(form)

        
    def form_invalid(self, form) :
        return super().form_invalid(form)


    def get_success_url(self) :
        return reverse_lazy('QuizApp:playquiz', kwargs={'slug':self.slug})
    

class Result(TemplateView):
    template_name = 'progress.html'


    def dispatch(self, request, *args, **kwargs) :
            self.slug = self.kwargs.get('slugs')
            quiz = get_object_or_404(Quiz,category = self.slug).quizId
            if UserAnswer.get_unanswered_question(user_id=self.request.user.UserId,quiz=quiz) != None:
                return redirect('QuizApp:quizlist')
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        
        context =  super().get_context_data(**kwargs)
        context['slug'] = self.request.path
        slug= self.kwargs.get('slugs')
        question_list = Question.objects.filter(quizId=Quiz.objects.get(category=slug).quizId).values_list('questionID')
        answer_list = UserAnswer.objects.filter(UserId = self.request.user.UserId, questionID__in = question_list)
        correct_Answers = CorrectAnswer.objects.filter( questionID__in = question_list,checkAnswerBool= 1)
        context['zipped_data'] =  zip(answer_list,correct_Answers)
        correct_answer_marks = UserAnswer.objects.filter(questionID__in = question_list,is_correct=1).aggregate(Sum('currentScore')) #marks received 
        context['received_marks'] = correct_answer_marks['currentScore__sum']
        total_marks = Question.objects.filter(questionID__in = question_list).aggregate(Sum('marks')) #total marks of all available questions
        context['total_marks'] = total_marks['marks__sum']
        return context
  

# def Mytest_view(request,slug):
#     print(request.method,'ooooooooooooooo')
#     quiz = get_object_or_404(Quiz,category = slug).quizId
#     user = request.user.UserId
#     if UserAnswer.get_unanswered_question(user_id=user,quiz=quiz) == None:
#         return redirect('QuizApp:result', result='result',slugs=slug)
        
#     question = UserAnswer.get_unanswered_question(user_id=user,quiz=quiz).first()
#     print('qustin before ', question)
#     if request.method == 'POST':
#         form = AnswerUSerForm(question=question,type=question.type,data = request.POST)
#         print('qustin after ', question)
#         if form.is_valid():
#             print('qustin after form valid ', question)
#             userChoosenOption = request.POST.get('textAnswer')
#             if request.POST.get('textAnswer') is not None:
#                     mcq = True
#                     try:
#                         uuid.UUID(userChoosenOption, version=4)
#                     except ValueError:
#                         mcq= False
                    
#                     print('MCQ is ', mcq)
#                     if mcq:

#                         checkAnswer = CorrectAnswer.objects.get(correctAnswerID = userChoosenOption).checkAnswerBool
#                         question_id = CorrectAnswer.objects.get(correctAnswerID = userChoosenOption).questionID_id
#                         question = Question.objects.get(questionID=question_id)
#                         if checkAnswer==True:
#                             marks = Question.objects.get(questionID = question_id).marks
#                             is_correct = True
#                         else:
#                             marks = 0
#                             is_correct = False

#                         currentScore = marks
#                         userID = user
#                         choosed_answer = CorrectAnswer.objects.get(correctAnswerID = userChoosenOption).answer
#                         UserAnswer.objects.create(  currentScore=currentScore,
#                                                     textAnswer = choosed_answer,
#                                                     UserId_id= userID,
#                                                     questionID= Question.objects.get(question = question) ,
#                                                     is_correct=is_correct
#                                                 )
                                                
                        

#                     else:
                        
#                         userGussedAnswer = request.POST.get('textAnswer')
#                         question_id =  question.questionID 
#                         question = Question.objects.get(questionID=question_id)
#                         answer_present = CorrectAnswer.objects.get(questionID=question_id).answer
#                         if answer_present.strip().lower() == userGussedAnswer.strip().lower():
                           
#                             find_marks = (Question.objects.filter(questionID = question_id).values('marks'))
#                             is_correct = True
#                             marks = int(find_marks[0]['marks'])
#                         else:
#                             marks = 0
#                             is_correct = False

#                         currentScore = marks
#                         userID = user
                        
#                         UserAnswer.objects.create(  currentScore=currentScore,
#                                                     textAnswer = userGussedAnswer,
#                                                     UserId_id= userID,
#                                                     questionID= Question.objects.get(question = question) ,
#                                                     is_correct=is_correct
#                                                  )
                                                
                        

#             else:
#                     question_id = question.questionID 
#                     question = Question.objects.get(questionID=question_id)
#                     marks = 0
#                     is_correct = False
#                     userID = user
#                     UserAnswer.objects.create(  currentScore=marks,
#                                                 textAnswer = 'Not Attempted',
#                                                 UserId_id= userID,
#                                                 questionID= Question.objects.get(question = question) ,
#                                                 is_correct=is_correct
#                                             )
                                                
                    
            
               
#         return redirect('QuizApp:playquiz',slug)
                    
#     else:
#         form = AnswerUSerForm(question=question,type=question.type)
#     return render(request,'game.html',{'form':form,'viewer_question':question})






