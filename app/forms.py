from django.core.exceptions import ValidationError
from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_check = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            raise ValidationError('Passwords do not match')

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        user = User.objects.create_user(**self.cleaned_data)
        profile = Profile.objects.create(user=user)
        profile.save()
        return user


    class Meta:
        model = User
        fields = ['username', 'email']


class CustomizeForm(forms.ModelForm):
    avatar = forms.ImageField(label='Avatar', required=False)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        if self.cleaned_data.get('avatar'):
            profile = user.profile
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()
        return user


    class Meta:
        model = User
        fields = ['username', 'email']


class AskForm(forms.Form):
    title = forms.CharField(label='Title')
    text = forms.CharField(label='Text', widget=forms.Textarea)
    tags = forms.CharField(label='Tags')

    def save(self, **kwargs):
        print(kwargs)
        # return Question.objects.create_question(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(label='Text', widget=forms.Textarea)
