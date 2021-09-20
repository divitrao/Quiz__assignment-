from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.forms import fields
from django.forms import widgets
from .models import UserAnswer
from django.forms.widgets import RadioSelect
from .models import CorrectAnswer, Progress


# class AnswerUSerForm(forms.ModelForm):
#     textAnswer = forms.ModelChoiceField(

#         queryset=CorrectAnswer.objects.none(),
#         widget= RadioSelect(),
#         required=False,
#         empty_label=None,
#         label=""
#     )

#     class Meta:
#         model = UserAnswer
#         fields = ('textAnswer',)
#         widgets  = {
#             'class' : 'btn-group btn-group-toggle'
#         }

#     def __init__(self,*args,**kwargs) :
#         question = kwargs.pop('question')
#         type = kwargs.pop('type')
#         print('hh')
#         super().__init__(*args,**kwargs)
#         if type=='mcq':
#             self.fields['textAnswer']   = forms.ChoiceField(choices=CorrectAnswer.objects.filter(questionID = question.questionID).values_list('correctAnswerID','answer'), widget= RadioSelect, required=False, label=" ")
#             self.fields['textAnswer'].label = " "
#         else:
#             self.fields['textAnswer'] = forms.CharField(max_length=20,required=False)






class AnswerForm(forms.ModelForm):
    textAnswer = forms.ModelChoiceField(queryset=CorrectAnswer.objects.none(),
                                        widget=RadioSelect,
                                        required=False,
                                        label=" "
                                        )

    class Meta:
        model = UserAnswer
        fields = ('textAnswer',)

    def clean(self) :
        return super(AnswerForm,self).clean()
        textAnswer = self.cleaned_data['textAnswer']


        
   
    def __init__(self,type,question,*args,**kwargs) :

        super(AnswerForm,self).__init__(*args,**kwargs)
        if type == 'mcq':
            
            self.fields['textAnswer']  = forms.ChoiceField(choices=CorrectAnswer.objects.filter(questionID = question.questionID).values_list('correctAnswerID','answer'), widget= RadioSelect, required=False, label="")
            self.fields['textAnswer'].widget.attrs.update({
                'class':'btn bg-light'
            })
            
                
          
            
        else:
            self.fields['textAnswer'] = forms.CharField(max_length=50, required=False,)
          

# class Addprogress(forms.ModelForm):
#     class Meta:
#         model = Progress
#         fields = ('minutes','seconds',)
                
           
        
        
    