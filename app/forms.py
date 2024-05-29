from typing import Any
from django import forms
from . import models
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super().clean()



class SignUpForm(forms.ModelForm):
    
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'password']
    
    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    

class AskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=models.Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = models.Question
        fields = ['title', 'text']

    def save(self, commit=True):
        ask = super().save(commit=True)
        ask.tags.set(self.cleaned_data['tags'])
        ask.save()
        return ask
        
class AnswerForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = models.Answer
        fields = ['text']
    def save(self, request, question_id, commit=True):
        answer = super().save(commit=False)
        answer.question_id = question_id
        answer.truth_checkbox = False
        author = request.user
        profile = models.Profile.objects.get(user_ptr=author)
        answer.author = profile
        answer.save()
        return answer
    

class EditForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'password']

    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Passwords do not match')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user