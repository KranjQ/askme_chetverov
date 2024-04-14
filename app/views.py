from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from . import models

QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": f"This is question number {i}",
        "id": i,
        "tag_id": f"{i}"    
    } for i in range(20)
]

ANSWERS = [
    {
        "title": f"Answer {i}",
        "text": f"It is answer on question {i}",
        "issue_id": i
    } for i in range(20)
]

TAGS = [
    {   "id": f"{i}",
        "name": f"Tag {i}"
    } for i in range(20)
]



def paginate(request, context_list):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(context_list, 4)
    page_obj = paginator.page(page_num)
    return page_obj

def index(request):
    questions = models.Question.objects.get_new()
    page_obj = paginate(request, questions)
    return render(request, "index.html", {"questions" : page_obj})

def hot(request):
    questions = models.Question.objects.get_hot()
    page_obj = paginate(request, questions)
    return render(request, "hot.html", {"questions" : page_obj})

def question(request, question_id):
    item = models.Question.objects.get(pk=question_id)
    answers = models.Answer.objects.filter(question=question_id)
    return render(request, "question.html", {"question": item, "answers": answers})

def tag(request, tag_id):
    tag = models.Tag.objects.get(pk=tag_id)
    questions = models.Tag.objects.get(pk=tag_id).question_set.all()
    return render(request, "bytag.html", {"tag": tag, "questions": questions})

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def ask(request):
    return render(request, "ask.html")

def settings(request):
    return render(request, "settings.html")

def not_auth(request):
    return render(request, "base_not_auth.html")