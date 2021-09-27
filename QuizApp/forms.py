from django import forms
from django.forms.widgets import RadioSelect
from .models import CorrectAnswer, UserAnswer
import time


class AnswerForm(forms.ModelForm):
    user_answer = forms.ModelChoiceField(queryset=CorrectAnswer.objects.none(),
                                        widget=RadioSelect,
                                        required=False,
                                        label=" "
                                        )

    class Meta:
        model = UserAnswer
        fields = ('user_answer',)


    def __init__(self,type,question,*args,**kwargs) :

        super(AnswerForm,self).__init__(*args,**kwargs)
        self.type = type
        if self.type == 'mcq':
            
            self.fields['user_answer']  = forms.ChoiceField(choices=CorrectAnswer.objects.filter(questionID = question.questionID).values_list('correctAnswerID','answer'), widget= RadioSelect, required=False, label="")
            self.fields['user_answer'].widget.attrs.update({
                'class':'btn bg-light'
            })
            
        else:
            self.fields['user_answer'] = forms.CharField(max_length=50, required=False,)

    def clean(self) :
        time.sleep(0.1)
        if self.type!='mcq':
            user_answer = self.cleaned_data['user_answer']
            if user_answer.strip().isalpha() is False and user_answer.strip().isnumeric() is False:
                if len(user_answer.strip())==0:
                    return super().clean()
                raise forms.ValidationError('No symbols allowed in answer')
            else:
                return super().clean()

    
        

          

