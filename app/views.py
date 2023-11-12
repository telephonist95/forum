from django.shortcuts import render
from django.core.paginator import Paginator


QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Question {i} content',
        'tags': [{'name': f'tag{i}'} for i in range(4)],
    } for i in range(100)
]

ANSWERS = [
    {
        'id': i,
        'title': f'Answer {i}',
        'content': f'Answer {i} content',
    } for i in range(100)
]


def paginate(objects, request, per_page=20):
    paginator = Paginator(objects, per_page)
    return paginator.page(request.GET.get('page', 1))


# Create your views here.
def index(request):
    return render(request, 'index.html', {'page': paginate(QUESTIONS, request)})


def hot(request):
    return render(request, 'index.html', {'page': paginate(QUESTIONS, request)})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def question(request, question_id):
    question = QUESTIONS[question_id]
    return render(request, 'question.html', {'page': paginate(ANSWERS, request), 'question': question})


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')


def tag(request, tag_name):
    return render(request, 'tag.html', {'questions': QUESTIONS, 'tag': tag_name})
