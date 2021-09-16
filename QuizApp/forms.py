from django import forms
from django.db.models.query import QuerySet
from django.forms import fields
from .models import UserAnswer
from django.forms.widgets import RadioSelect
from .models import CorrectAnswer

class AnswerForm(forms.ModelForm):
    textAnswer = forms.ModelChoiceField(queryset=CorrectAnswer.objects.none(),
                                        widget=RadioSelect,
                                        required=False,
                                        )

    class Meta:
        model = UserAnswer
        fields = ('textAnswer',)

    def clean(self) :
        return super(AnswerForm,self).clean()
        textAnswer = self.cleaned_data['textAnswer']
        
   
    def __init__(self,type,question,*args,**kwargs) :
        
        super(AnswerForm,self).__init__(*args,**kwargs)
        print('111111111111111111111111111111111111111111111111111111111111111111111111111111')
        print('from form',question)
        print('from form',question.questionID)
        # print('xxxxxxxxxx',CorrectAnswer.get_answer_list(self,question.questionID))
        options = [x for x in CorrectAnswer.get_answer_list(self,question.questionID)]
        # print(options)
        if type == 'mcq':
            
            self.fields['textAnswer']  = forms.ChoiceField(choices=CorrectAnswer.objects.filter(questionID = question.questionID).values_list('correctAnswerID','answer'), widget= RadioSelect, required=False, label=None)
            self.fields['get_id'] = forms.CharField(max_length=37,required=False)
            self.fields['get_id'].widget.attrs.update({
                'value': question.questionID,
                
            })
            
        else:
            self.fields['textAnswer'] = forms.CharField(max_length=50, required=False,)
            self.fields['get_id'] = forms.CharField(max_length=37,required=False)
            self.fields['get_id'].widget.attrs.update({
                'value': question.questionID,
                
            })
           
        
        
    