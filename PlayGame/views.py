from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.http.response import JsonResponse
from QuizApp.models import Answer, Quiz, UserAnswer, Question, Progress, Results
import json
import math

class QuizListView(TemplateView):
    template_name = 'quiz_subject_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('playagain') == 'True':
            subject = request.GET.get('subject')
            UserAnswer.objects.filter(user=request.user.id, question__quiz__category=subject).delete()
            Progress.objects.filter(user=request.user.id, subject=subject).delete()
        return super().dispatch(request, *args, **kwargs)


class GameView(TemplateView):
    template_name = 'game.html'

    def dispatch(self, request, *args, **kwargs):
        user_answered_question = UserAnswer.objects.filter(user=request.user.id , 
                                                        question__quiz__category=request.GET.get('subject'))\
                                                        .values_list('question')
        user_unanswered_questions = Question.objects.filter(quiz__category=request.GET.get('subject'))\
                                                                .exclude(id__in=user_answered_question)
        if len(user_unanswered_questions) == 0:
            return redirect('PlayGame:result', slugs=request.GET.get('subject'), exam_number=1)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        exam_time = Quiz.objects.get(category=self.request.GET.get('subject')).alloted_time
        if UserAnswer.objects.filter( user=self.request.user.id , 
                                      question__quiz__category=self.request.GET.get('subject')).exists():
            exam_number = len(set(Results.objects.filter(user=self.request.user.id , 
                                                        question__quiz__category=self.request.GET.get('subject'))\
                                                        .values_list('exam_number'))) 
        else:
             exam_number = len(set(Results.objects.filter(user = self.request.user.id , 
                                                         question__quiz__category=self.request.GET.get('subject'))\
                                                         .values_list('exam_number'))) + 1
        context['extra_data'] = json.dumps({'alloted_time':exam_time,
                                            'exam_number':exam_number})
        return context

    
class ResultView(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result_count = Results.objects.filter(user=self.request.user.id, 
                                              question__quiz__category=self.kwargs.get('slugs')).count()
        question_count = Question.objects.filter(quiz__category=self.kwargs.get('slugs')).count()
        if result_count % question_count == 0:
            total_results = int(result_count/question_count)
        else:
            total_results = math.floor(result_count/question_count)
        
        context['subject'] = self.kwargs.get('slugs')
        context['exam_number'] = self.kwargs.get('exam_number')
        context['extra_data'] = json.dumps({ 
                                             'subject':self.kwargs.get('slugs'),
                                             'exam_number':self.kwargs.get('exam_number'),
                                             'total_result':total_results
                                              })
        return context


class UpdateToDatabase(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.is_ajax:
            if request.POST.get('is_correct') == 'true':
                is_correct = True
            else:
                is_correct = False
            UserAnswer.objects.create(
                                        user_id=request.user.id,
                                        question_id=Question.objects.get(id=request.POST.get('question')).id,
                                        user_answer=request.POST.get('text_answer'),
                                        is_correct=is_correct,
                                        current_score=int(request.POST.get('marks')))

            correct_answer = Answer.objects.get(question = request.POST.get('question'),check_answer_bool=1).options
            
            Results.objects.create(
                                        user_id=request.user.id,
                                        question_id=Question.objects.get(id=request.POST.get('question')).id,
                                        user_answer=request.POST.get('text_answer'),
                                        correct_answer=correct_answer,
                                        marks_achieved=int(request.POST.get('marks')),
                                        exam_number=int(request.POST.get('exam_number')),
                                        question_text=Question.objects.get(id=request.POST.get('question')).question



            )


            
            return JsonResponse({},status = 200)


class UpdateTime(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.is_ajax:
            if Progress.objects.filter(user=request.user.id , subject=request.POST.get('subject')).exists():
                existing_question = Progress.objects.get(user=request.user.id , subject = request.POST.get('subject'))
                existing_question.question_id = Question.objects.get(id=request.POST.get('question_id'))
                existing_question.minutes = int(request.POST.get('minute'))
                existing_question.seconds = int(request.POST.get('second'))
                existing_question.save()
            else:
                Progress.objects.create(
                                         user_id=request.user.id,
                                         question_id=Question.objects.get(id = request.POST.get('question_id')).id,
                                         subject=request.POST.get('subject'),
                                         minutes=int(request.POST.get('minute')),
                                         seconds=int(request.POST.get('second')) )

               

        return JsonResponse({},status=200)




