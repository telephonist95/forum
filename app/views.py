from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *


def paginate(objects, request, per_page=20):
    paginator = Paginator(objects, per_page)
    return paginator.page(request.GET.get('page', 1))


def index(request):
    questions = Question.objects.with_rating().order_by('created')
    return render(request, 'index.html', {'page': paginate(questions, request)})


def hot(request):
    questions = Question.objects.with_rating().order_by('-rating')
    return render(request, 'index.html', {'page': paginate(questions, request)})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def question(request, question_id):
    question = Question.objects.with_rating().get(id=question_id)
    answers = Answer.objects.with_rating().filter(question=question).order_by('created')
    return render(request, 'question.html', {'page': paginate(answers, request), 'question': question})


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')


def tag(request, tag_name):
    questions = Question.objects.with_rating().filter(tags__name=tag_name)
    return render(request, 'tag.html', {'page': paginate(questions, request), 'tag': tag_name})
