# External Libaries(outside of Django)
import json
# Django Libaries
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

# Django Models
from .models import Question
from .models import Answer
from .models import User

# Django Forms
from .forms import RegisterForm
from .forms import AskForm

def index(request):
    question = Question.objects.get(pk = 1)
    user = User.objects.get(pk = 1)
    return render(request, "codesphere/index.html")


def login_view(request):
  if request.method == "POST":
    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
    else:
      return render(request, "codesphere/login.html", {
          "message": "Invalid username and/or password."
      })
  else:
    return render(request, "codesphere/login.html")

@login_required
def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))


def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
      return render(request, "codesphere/register.html", {
        "message": "Passwords must match.",
        "form": RegisterForm()
      })

    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      #user.save()
    except IntegrityError:
      return render(request, "codesphere/register.html", {
      "message": "Username already taken.",
      "form": RegisterForm()
    })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
  else:
    return render(request, "codesphere/register.html", {
      "form": RegisterForm()     
    })

@login_required
def ask(request):
  return render(request, "codesphere/ask.html", {
    # Create the form from forms.py
    "form": AskForm()
  })

def forum(request):
  # Output all questions to forum page
  data = Question.objects.all()
  return render(request, "codesphere/forum.html", {"questions":data})

def display(request, _question):
  # Display the question
  question = Question.objects.get(pk=_question)
  #Display all answwers with the answwered id corresponding to the questions id
  answers = Answer.objects.filter(answered__id__exact = _question)
  return render(request, "codesphere/display.html", {"question": question, "answers": answers})

# Api for /ask.html
# NOT REST (no JSON response)
@login_required
def apiask(request):
  if request.method == "POST":
    form = AskForm(request.POST)
    if form.is_valid():
      _user = request.user
      _question = form.cleaned_data["question"]
      _content = form.cleaned_data["content"]
      post = Question.objects.create(asker = _user, question = _question, content = _content)
      post.save()
      url = "display";
      return redirect(reverse(url, kwargs={"_question": post.pk}))

# Api for /display.html answer form
# NOT REST (no JSON response)
@login_required
def apians(request): 
  if request.method == "POST":
    _user = request.user;
    _content = request.POST["content"]
    _id = request.POST["id"]
    _question = Question.objects.get(pk=_id)
    form = Answer.objects.create(replier = _user, content = _content, answered = _question)
    form.save()
    url = "display";
    return redirect(reverse(url, kwargs={"_question": _id}))

# Api for upvoting(full focumentation bellow)
"""
REST API PUT request /api/up/<question_id>

In:
{
  upvote: boolean
  (false: downvote)
  (true: upvote)
}
Out:
{
  success: boolean
}
First check if the user has downvoted by checking the many to many field of donwvotes. If the user has downvoted already, then the upvote will change the number to a neutral one, so remove the downvoted relation. Otherwise, add a relation to the upvotes. Same for the donwvotes, check if there is a relation to the question in the upvotes, if not then add relation, else don't.

IF upvote: true
  IF question in downvoted
    remove question from downvoted
  ELSE 
    add question to upvoted
IF upvote: false
  IF question in upvoted
    remove question from upvoted
  ELSE
    add question to downvoted

API GET request /api/up/<question_id>

In:
{}
Out:
{
  upvotes: integer,
  upvoted: boolean,
  success: boolean
}

NOTICE: THE SYSTEM IS THE SAME FOR THE ANSWER UPVOTES AS WELL
""" 

@login_required
def apiup(request, _question):  
  put = json.loads(request.body)
  if request.method == "PUT":
    question = Question.objects.get(pk=_question)
    # print(question)
    user = request.user
    if put.get("upvote") == True:
      if not question in request.user.upvoted.all():
        if not question in request.user.downvoted.all():
          question.upvotes = question.upvotes + 1
          user.upvoted.add(question)
          print("+")
        else:
          question.upvotes = question.upvotes + 1
          user.downvoted.remove(question)
      else:
        question.upvotes = question.upvotes - 1
        user.upvoted.remove(question)
        print("-")
    else:
      if not question in request.user.downvoted.all():
        if not question in request.user.upvoted.all():
          question.upvotes = question.upvotes - 1
          user.downvoted.add(question)
          print("+")
        else:
          question.upvotes = question.upvotes - 1
          user.upvoted.remove(question)
          print("+")
      else:
        question.upvotes = question.upvotes + 1
        user.downvoted.remove(question)
        print("-")
    try:
      question.save()
      user.save()
    except:
      print("An exception occured...")
      return JsonResponse({
        "success": False
      })
    return JsonResponse({
      "success": True
    })
  elif request.method == "GET":
    return JsonResponse({
      "upvotes": Question.objects.get(pk=_question).upvotes,
      "upvoted": request.user.upvoted.filter(pk=_question).exists(),
      "success": True
    })
  else:
    print("smh:")
    return JsonResponse({
      "success": False
    })

@login_required
def apiaup(request, _question):
  put = json.loads(request.body)
  print(put)
  # if not request.user in thread.participants.all():
  # question = "none"
  if request.method == "PUT":
    # print(request.POST["upvote"])
    print("PUT")
    print(put)
    print(put.get('upvote'))
    answer = Answer.objects.get(pk=_question)
    print(answer)
    user = request.user
    if put.get("upvote") == True:
      if not answer in request.user.answer_upvoted.all():
        # if request.user.upvoted.get(pk = _question).exists() is None:
        answer.upvotes = answer.upvotes + 1
        user.answer_upvoted.add(answer)
        print("+")
    else:
      if answer in request.user.answer_upvoted.all():
        answer.upvotes = answer.upvotes - 1
        user.answer_upvoted.add(answer)
        print("+")
    try:
      answer.save()
      user.save()
    except:
      print("An exception occured...")
      return JsonResponse({
        "success": False
      })
    return JsonResponse({
      "success": True
    })
  elif request.method == "GET":
    return JsonResponse({
      "upvotes": Question.objects.get(pk=_question).upvotes,
      "upvoted": request.user.upvoted.filter(pk=_question).exists(),
      "success": True
    })
  else:
    print("smh:")
    return JsonResponse({
      "success": False
    })

@csrf_exempt
def apisearch(request):
  post = json.loads(request.body)
  query = post.get("query")
  print(query)
  question = Question.objects.filter(content__contains = query)
  answer = Answer.objects.filter(answered = question)
  return JsonResponse({
    "question": question,
    "answers": answer
  })
