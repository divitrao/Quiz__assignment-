from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .models import Quiz, Question, UserAnswer, CorrectAnswer, Progress
from .forms import AnswerForm 
from django.urls import reverse_lazy
import uuid
from django.db.models import Sum
from json import dumps
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View


@method_decorator(login_required, name='dispatch')
class QuizList(ListView):
    model = Quiz
    template_name = 'quizzList.html'
    context_object_name = 'quizlists'

    def dispatch(self, request, *args, **kwargs):
        
        if request.GET.get('playagain') == 'True':
            subject = request.GET.get('slug')
            quiz = Quiz.objects.get(category=subject.lower()).quizId
            question_list = Question.objects.filter(quizId=quiz)\
                            .values_list('questionID')
            UserAnswer.objects.filter(questionID__in=question_list,
                                      UserId=request.user.UserId).delete()
            Progress.objects.filter(subject=subject.lower(),
                                    UserId=request.user.UserId).delete()
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_display_list = []
        context['quizlists'] = Quiz.objects.all()
        quiz_list = Quiz.objects.all().values('category')
        for subjects in quiz_list:
            quiz_display_object = {}
            try:
                unanswered_question_length = len(UserAnswer.get_unanswered_question(self = self, 
                                                    user_id = self.request.user.UserId,
                                                  quiz = Quiz.objects.get(category = subjects['category']).quizId) )
                                               
            except:
                unanswered_question_length = 0

            quiz_display_object['total_question'] = Question.objects.filter(quizId=Quiz.objects.get(category=subjects['category']).quizId ).count()
            quiz_display_object['quiz_description'] = Quiz.objects.get(category = subjects['category']).quizDescription
            quiz_display_object['pending_question'] = unanswered_question_length
            quiz_display_object['slugs'] = Quiz.objects.get(category=subjects['category']).slug
            quiz_display_object['time'] = Quiz.objects.get(category=subjects['category']).alloted_time
            quiz_display_list.append(quiz_display_object)
        context['zippedData'] = quiz_display_list
        return context


@method_decorator(login_required, name='dispatch')
class PlayQuiz(FormView):
    form_class = AnswerForm
    template_name = 'game.html'


    def dispatch(self, request, *args, **kwargs):
        self.slug = self.kwargs.get('slug')
        quiz = get_object_or_404(Quiz,category=self.slug).quizId  
        if UserAnswer.get_unanswered_question(self = self, user_id=self.request.user.UserId, quiz=quiz) is None:
            return redirect('QuizApp:result', result='result', slugs=self.slug)
        return super().dispatch(request, *args, **kwargs)

    
    def get_form(self, *args, **kwargs):
            self.unanswered_question = UserAnswer.get_unanswered_question(self = self, user_id = self.request.user.UserId,
                                                                          quiz = Quiz.objects.get(category=self.slug).quizId)                                                              
            self.question = self.unanswered_question.first()
            self.type = self.question.type
            return self.form_class(**self.get_form_kwargs())


    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        return dict(kwargs,question = self.question, type = self.type)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Progress.objects.filter(UserId=self.request.user.UserId,
                                   subject=self.slug,
                                   questionID=self.question.questionID).exists():

                pending_question = Progress.objects.get(UserId=self.request.user.UserId,
                                                        subject=self.slug,
                                                        questionID=self.question.questionID
                                                        )
                minute = pending_question.minutes
                seconds = pending_question.seconds
        else:
            minute = Quiz.objects.get(slug=self.slug).alloted_time
            seconds = 0  
        data = {
                    'question_id': self.question.questionID.hex,
                    'user_id': self.request.user.UserId.hex,
                    'minute': minute,
                    'second': seconds,
                    'subject': self.slug}                  
        context['viewer_question'] = self.question
        context['data'] = dumps(data)
        return context

   
    def form_valid(self, form):
        user = self.request.user.UserId
        userChoosenOption = form.cleaned_data['textAnswer']
        if userChoosenOption is not None and len(userChoosenOption.strip())!=0:
            mcq = True
            try:
                uuid.UUID(userChoosenOption, version=4)
            except ValueError:
                mcq= False
            if mcq:

                checkAnswer = CorrectAnswer.objects.get(correctAnswerID=userChoosenOption).checkAnswerBool
                question_id = CorrectAnswer.objects.get(correctAnswerID=userChoosenOption).questionID_id # questionID_id is name of column in database
                question = Question.objects.get(questionID=question_id)
                if checkAnswer is True:
                        marks_mcq = Question.objects.get(questionID=question_id).marks
                        is_correct = True
                else:
                        marks_mcq = 0
                        is_correct = False
                userID = user
                choosed_answer = CorrectAnswer.objects.get(correctAnswerID=userChoosenOption).answer
                UserAnswer.objects.create( currentScore=marks_mcq,
                                           textAnswer=choosed_answer,
                                           UserId_id=userID,
                                           questionID=Question.objects.get(question=question) ,
                                           is_correct=is_correct
                                        )        

            else:
                            
                        userGussedAnswer = self.request.POST.get('textAnswer')
                        question_id =  self.question.questionID
                        question = Question.objects.get(questionID=question_id)
                        answer_present = CorrectAnswer.objects.get(questionID=question_id).answer
                        if answer_present.strip().lower() == userGussedAnswer.strip().lower():
                            
                            marks_oneword= Question.objects.get(questionID = question_id).marks
                            is_correct = True
                        else:
                            marks_oneword = 0
                            is_correct = False

                        userID = user
                        UserAnswer.objects.create(  currentScore=marks_oneword,
                                                    textAnswer = userGussedAnswer,
                                                    UserId_id= userID,
                                                    questionID= Question.objects.get(question = question) ,
                                                    is_correct=is_correct
                                                )
        else:
                        question_id =  self.question.questionID
                        question = Question.objects.get(questionID=question_id)
                        userID = user
                        UserAnswer.objects.create(  currentScore=0,
                                                    textAnswer = 'Not Attempted',
                                                    UserId_id= userID,
                                                    questionID= Question.objects.get(question = question),
                                                    is_correct=False)
                                                 
        return super().form_valid(form)

    def get_success_url(self) :
        return reverse_lazy('QuizApp:playquiz', kwargs={'slug':self.slug})
    

@method_decorator(login_required,name='dispatch')
class Result(TemplateView):
    template_name = 'progress.html'


    def dispatch(self, request, *args, **kwargs):
            self.slug = self.kwargs.get('slugs')
            quiz = get_object_or_404(Quiz,category = self.slug).quizId
            if UserAnswer.get_unanswered_question(self = self, user_id=self.request.user.UserId,quiz=quiz) != None:
                return redirect('QuizApp:quizlist')
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        
        '''
        Result page , it is collecting all questions,
        there correct answer and user answer, also collecting 
        sums of marks achieved

        '''
        
        context =  super().get_context_data(**kwargs)
        slug= self.kwargs.get('slugs')
        question_list = Question.objects.filter(quizId=Quiz.objects.get(category=slug).quizId).values_list('questionID')
        answer_list = UserAnswer.objects.filter(UserId = self.request.user.UserId, questionID__in = question_list)
        correct_Answers = CorrectAnswer.objects.filter( questionID__in=question_list,checkAnswerBool=1)
        context['zipped_data'] =  zip(answer_list,correct_Answers)
        correct_answer_marks = UserAnswer.objects.filter(questionID__in=question_list,UserId = self.request.user.UserId).aggregate(Sum('currentScore'))
        context['received_marks'] = correct_answer_marks['currentScore__sum']
        total_marks = Question.objects.filter(questionID__in=question_list).aggregate(Sum('marks')) #total marks of all available questions
        context['total_marks'] = total_marks['marks__sum']
        context['slug'] = slug.upper()
        context['zipped_data_js'] =  dumps({
                                            'user_answer': list(UserAnswer.objects.filter(UserId=self.request.user.UserId, questionID__in=question_list).values('textAnswer')),
                                            'correct_answer': list(CorrectAnswer.objects.filter( questionID__in=question_list,checkAnswerBool=1).values('answer'))
                                             })
        return context


class UpdateTime(View):
    def dispatch(self, request) :
        if request.method == 'POST' and request.is_ajax:
            if Progress.objects.filter(UserId=request.user.UserId,
                                       subject=request.POST.get('subject')).exists():
                                     
                existing_question=Progress.objects.get(UserId=request.user.UserId,subject=request.POST.get('subject'))
                existing_question.questionID_id=Question.objects.get(questionID = request.POST.get('questionid'))
                existing_question.minutes=int(request.POST.get('minute'))
                existing_question.seconds=int(request.POST.get('seconds'))
                existing_question.save()
            else:
                Progress.objects.create(
                                        UserId_id=request.user.UserId,
                                        subject=request.POST.get('subject'),
                                        questionID=Question.objects.get(questionID = request.POST.get('questionid')),
                                        minutes=int(request.POST.get('minute')),
                                        seconds=int(request.POST.get('seconds'))
                                        )
            return JsonResponse({},status = 200)








