from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods 
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from . import models
from . import forms

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
    if request.method == 'GET':
        answer = forms.AnswerForm()
    if request.method == "POST":
        answer = forms.AnswerForm(data=request.POST)
        if answer.is_valid():
            answer.save(request=request, question_id=question_id)
    item = models.Question.objects.get(pk=question_id)
    answers = models.Answer.objects.get_order_by_answers()
    page_obj = paginate(request, answers)
    

    return render(request, "question.html", {"question": item, "answers": page_obj, "form" : answer})

def tag(request, tag_id):
    tag = models.Tag.objects.get(pk=tag_id)
    questions = models.Tag.objects.get(pk=tag_id).question_set.all()
    return render(request, "bytag.html", {"tag": tag, "questions": questions})

@require_http_methods(["GET", "POST"])
def login_user(request):

    if request.method == 'GET':
        login_form = forms.LoginForm()
    if request.method == 'POST':
        login_form = forms.LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
    return render(request, "login.html", context={"form": login_form})

def signup(request):
    if request.method == 'GET':
        signup_form = forms.SignUpForm()
    if request.method == 'POST':
        signup_form = forms.SignUpForm(data=request.POST, files=request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                signup_form.add_error(filed = None, error = "User saving error")
            
    return render(request, "signup.html", context={"form":signup_form})

@login_required
def ask(request):
    print(request.user)
    if request.method == "GET":
        ask_form = forms.AskForm()
    if request.method == 'POST':
        ask_form = forms.AskForm(data=request.POST)
        if ask_form.is_valid():
            question = ask_form.save(commit=False)
            profile = models.Profile.objects.get(user_ptr=request.user)
            print(profile)
            question.author = profile
            question.save()
        if question:
            return redirect(reverse('index'))
        else:
            ask_form.add_error(field=None, error="Ask saving error")

    return render(request, "ask.html", context = {'form' : ask_form})

def settings(request):
    if request.method == 'GET':
        edit_form = forms.EditForm()
    if request.method == 'POST':
        current_user = models.Profile.objects.get(user_ptr_id=request.user.id)
        edit_form = forms.EditForm(data=request.POST, files=request.FILES, instance=current_user)
        if edit_form.is_valid():
            user = edit_form.save()
            if user:
                login(request, current_user)
                return render(request, "settings.html", context={"form" : edit_form})
                
            else:
                edit_form.add_error(filed = None, error = "User saving error")
            
    return render(request, "settings.html", context={"form" : edit_form})
    

def not_auth(request):
    return render(request, "base_not_auth.html")

@require_http_methods(["POST", "GET"])
@csrf_protect
def like_async(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    profile, profile_created = models.Profile.objects.get_or_create(user_ptr = request.user)
    question_like, question_like_created = models.QuestionLike.objects.get_or_create(question = question, user = profile)
    if not question_like_created:
        question_like.delete()
    return JsonResponse({ 'likes_count' : models.QuestionLike.objects.filter(question=question).count()})
def like_async_hot(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    profile, profile_created = models.Profile.objects.get_or_create(user_ptr = request.user)
    question_like, question_like_created = models.QuestionLike.objects.get_or_create(question = question, user = profile)
    if not question_like_created:
        question_like.delete()
    return JsonResponse({ 'likes_count' : models.QuestionLike.objects.filter(question=question).count()})

@require_http_methods(["POST", "GET"])
@csrf_protect
def like_async_answer(request, answer_id):
    answer = get_object_or_404(models.Answer, pk=answer_id)
    profile, profile_created = models.Profile.objects.get_or_create(user_ptr = request.user)
    answer_like, answer_like_created = models.AnswerLike.objects.get_or_create(answer = answer, user = profile)
    if not answer_like_created:
        answer_like.delete()
    return JsonResponse({ 'likes_count' : models.AnswerLike.objects.filter(answer=answer).count()})

def checkbox_async_answer(request, answer_id):
    answer = get_object_or_404(models.Answer, pk=answer_id)
    if answer.truth_checkbox:
        answer.truth_checkbox = False
    else:
        answer.truth_checkbox = True
    checked_status = int(answer.truth_checkbox)
    answer.save()
    return JsonResponse({ 'truth_checkbox' : checked_status})
def logout_user(request):
    logout(request)
    return redirect(reverse('index'))
