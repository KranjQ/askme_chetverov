from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from . import models
# Create your views here.



# cписок новых вопросов (главная страница) (URL = /)
# cписок “лучших” вопросов (URL = /hot/) сделано
# cписок вопросов по тэгу (URL = /tag/blablabla/) сделано  
# cтраница одного вопроса со списком ответов (URL = /question/35/) сделано 
# форма логина (URL = /login/) сделано
# форма регистрации (URL = /signup/) сделано 
# форма создания вопроса (URL = /ask/) AskMeсделано 

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
    # page_num = request.GET.get('page', 1)
    # paginator = Paginator(questions, 4)
    # page_obj = paginator.page(page_num)
    page_obj = paginate(request, questions)
    return render(request, "index.html", {"questions" : page_obj})

def hot(request):
    questions = models.Question.objects.get_hot()
    # page_num = request.GET.get('page', 1)
    # paginator = Paginator(questions, 4)
    # page_obj = paginator.page(page_num)
    page_obj = paginate(request, questions)
    return render(request, "hot.html", {"questions" : page_obj})

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, "question.html", {"question": item, "answers": ANSWERS})

def tag(request, tag_id):
    tag = TAGS[tag_id]
    return render(request, "bytag.html", {"tag": tag, "questions": QUESTIONS})

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