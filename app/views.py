from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.forms.models import model_to_dict
from django.http import JsonResponse

from .models import *
from .forms import *


def paginate(objects, request, per_page=20):
    paginator = Paginator(objects, per_page)
    try:
        return paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        return paginator.page(1)


def index(request):
    questions = Question.objects.newest()
    return render(request, 'index.html', {'page': paginate(questions, request)})


def hot(request):
    questions = Question.objects.hot()
    return render(request, 'index.html', {'page': paginate(questions, request)})


def ask(request):
    ask_form = AskForm()
    if request.method == 'POST':
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            print(request.user)
            ask_form.save()
    return render(request, 'ask.html', {'form': ask_form})


def login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                dj_login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error('password', 'Wrong password or username')
    return render(request, 'login.html', {'form': login_form})


def logout(request):
    dj_logout(request)
    return redirect(reverse('login'))


def signup(request):
    signup_form = SignupForm()
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                return redirect(request.GET.get('continue', '/'))
            else:
                signup_form.add_error(None, 'User saving error')
    return render(request, 'signup.html', {'form': signup_form})


def question(request, question_id):
    question = Question.objects.by_id(question_id)
    answers = Answer.objects.to_question(question)

    answer_form = AnswerForm()
    return render(request, 'question.html',
                  {'page': paginate(answers, request), 'question': question, 'form': answer_form})


def settings(request):
    customize_form = CustomizeForm(initial=model_to_dict(request.user))
    if request.method == 'POST':
        customize_form = CustomizeForm(request.POST, request.FILES, instance=request.user)
        if customize_form.is_valid():
            customize_form.save()
    return render(request, 'settings.html', {'form': customize_form})


def tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    return render(request, 'tag.html',
                  {'page': paginate(questions, request),
                   'tag': tag_name})


def question_react(request):
    question_id = request.POST.get('id')
    reaction_type = request.POST.get('type')
    question = get_object_or_404(Question, question_id)
    if reaction_type == 'like':
        QuestionReaction.objects.like(user=request.user, question=question)
    else:
        QuestionReaction.objects.deslike(user=request.user, question=question)

    return JsonResponse({})
    
