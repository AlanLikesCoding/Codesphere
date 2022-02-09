
# External Libaries(outside of Django)
import json
import os
# Geolocation
from json import load
from urllib.request import urlopen
from .libs import generate_token
from .libs import Colors
# Django Libaries
# Django core
from django.core.mail import send_mail
from django.core import serializers
from django.core.exceptions import ValidationError
# Django contrib
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
# Django shortcuts
from django.shortcuts import render
from django.shortcuts import redirect
# Django ultils
from django.utils.http import urlencode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes 
# Other
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.template.loader import render_to_string, get_template

# Django Models
from .models import Question
from .models import Answer
from .models import User

# Django Forms
from .forms import LoginForm
from .forms import RegisterForm
from .forms import AskForm
from .forms import AboutForm

# Basic
import os
import sys
import platform

# System Info
uname = platform.uname()
print(Colors.GREEN + "[SYSTEM]" + Colors.ENDC)
print("System: " + uname.system)
print("Node Name: " + uname.node)
print("Release: " + uname.release)
print("Version: " + uname.version)
print("Machine: " + uname.machine)
print("Processor: " + uname.processor)

# System Start
print(Colors.GREEN + Colors.BOLD + "[SYSTEM]" + Colors.ENDC + " System has started to run, the Codesphere server is up.")

print(Colors.GREEN + Colors.BOLD + "[DJANGO SYSTEM]" + Colors.ENDC)

def index(request):
    question = Question.objects.get(pk = 1)
    user = User.objects.get(pk = 1)
    return render(request, "codesphere/index.html")


def login_view(request):
  if request.method == "POST":
    form = LoginForm(request.POST)
    if form.is_valid():
      __username = form.cleaned_data["username"]
      __password = form.cleaned_data["password"]
      user = authenticate(request, username = __username, password = __password)
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
    else:
      return render(request, "codesphere/login.html", {
      "form": LoginForm(),
      "message": "Invalid username and/or password."
    })
  else:
    return render(request, "codesphere/login.html", {
      "form": LoginForm()
    })

@login_required
def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))


def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form.is_valid():
      __username = form.cleaned_data["username"]
      __email = form.cleaned_data["email"]
      __password = form.cleaned_data["password"]
      __confirmation = form.cleaned_data["confirmation"]
      # Check if username exists
      if User.objects.filter(username = __username).exists():
        return render(request, "codesphere/register.html", {
          "form": RegisterForm(),
          "message": "This username has already been taken, please choose a different username."
        })
      # Check if password exists
      elif __password != __confirmation:
        return render(request, "codesphere/register.html", {
          "form": RegisterForm(),
          "message": "Your password doesn't match your confirmation password."
        })
      # Begin making account
      else:
        # Email verification
        user = User.objects.create_user(__username, __email, __password)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('codesphere/email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'id': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })
        send_mail(mail_subject, message, 'support@codesphere.org', [__email])
        return HttpResponse('Please confirm your email address to complete the registration')
  else:
    return render(request, "codesphere/register.html", {
      "form": RegisterForm()     
    })

def activate(request, uidb64, token):
  User = get_user_model()
  try:
    id = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=id)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.save()
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
  else:
    return HttpResponse('Activation link is invalid!')

# About the User
def about(request, _user):
  data = User.objects.get(pk = _user)
  questions = Question.objects.filter(asker = data)
  # Get user location for the bio
  url = 'https://ipinfo.io/json'
  res = urlopen(url)
  location = load(res)
  # Check if user is editing their profile
  if (request.method == "POST"):
    user = request.user
    # Check if user is valid
    if user is not None and user.pk == _user:
      form = AboutForm(request.POST, request.FILES)
      if form.is_valid():
        # Check if use uploaded file
        if "upload" in request.FILES:
          # Filefield
          picture = request.FILES["upload"]
          # Paths
          base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
          path = "/media/profile/" + str(_user) + ".jpeg"
          # Create File
          directory = os.path.join(base, "codesphere" + path)
          open(directory, "wb+").write(picture.file.read())       
          user.picture = path
        # Get bio data
        bio = form.cleaned_data["bio"]
        user.bio = bio
        # Save the use form
        user.save()

        return render(request, "codesphere/edit_about.html", {
          "user": data,
          "location": location,
          "question": questions,
          "form": AboutForm({"bio": request.user.bio})
        })
      else:
        print("form no valuid")
    # If there is a proccessing error
    else:
      return render(request, "codesphere/about.html", {
        "user": data,
        "location": location,
        "question": questions,
        "form": AboutForm({"bio": request.user.bio}),
        "message": "Error, we have had some trouble proccessing you uploads, please try again later..."
      })
  # Check if this is the profile of the user
  if request.user is not None and request.user.pk == _user:
    return render(request, "codesphere/edit_about.html", {
      "user": data,
      "location": location,
      "question": questions,
      "form": AboutForm({"bio": request.user.bio})
    })
  # If user isn't logged in
  return render(request, "codesphere/about.html", {
    "user": data,
    "location": location,
    "question": questions
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
  return render(request, "codesphere/forum.html", {
    "questions": data
  })

def display(request, _question):
  # Display the question
  question = Question.objects.get(pk=_question)
  #Display all answwers with the answwered id corresponding to the questions id
  answers = Answer.objects.filter(answered__id__exact = _question)
  return render(request, "codesphere/display.html", {
    "question": question, 
    "answers": answers
  })

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

# Api for upvoting(full documentation bellow)
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
      "downvoted": request.user.downvoted.filter(pk=_question).exists(),
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
  if request.method == "PUT":
    answer = Answer.objects.get(pk=_question)
    user = request.user
    if put.get("upvote") == True:
      if not answer in request.user.answer_upvoted.all():
        if not answer in request.user.answer_downvoted.all():
          answer.upvotes = answer.upvotes + 1
          user.answer_upvoted.add(answer)
          print("+")
        else:
          answer.upvotes = answer.upvotes + 1
          user.answer_downvoted.remove(answer)
      else:
        answer.upvotes = answer.upvotes - 1
        user.answer_upvoted.remove(answer)
        print("-")
    else:
      if not answer in request.user.answer_downvoted.all():
        if not answer in request.user.answer_upvoted.all():
          answer.upvotes = answer.upvotes - 1
          user.answer_downvoted.add(answer)
          print("+")
        else:
          answer.upvotes = answer.upvotes - 1
          user.answer_upvoted.remove(answer)
          print("+")
      else:
        answer.upvotes = answer.upvotes + 1
        user.answer_downvoted.remove(answer)
        print("-")
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
      "upvotes": Answer.objects.get(pk=_question).upvotes,
      "upvoted": request.user.answer_upvoted.filter(pk=_question).exists(),
      "downvoted": request.user.answer_downvoted.filter(pk=_question).exists(),
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
  data = post.get("data")
  query = data.get("query")
  question = None
  if Question.objects.filter(content__icontains = query).exists() == False:
    question = Question.objects.filter(question__icontains = query)
  else:
    question = Question.objects.filter(content__icontains = query)
  answer = Answer.objects.filter(answered = question.first())
  if question is None or question.exists() == False:
    return JsonResponse({
      "question": "none",
      "content": "none"
    })
  else:
    question = question.first()
    if answer.count == 0:
      return JsonResponse({
        "question": question.question,
        "content": question.content
      })
    else:
      amount = []
      for i in answer:
        amount.append(i.content)
      answer_json = json.dumps(amount)
      return JsonResponse({
        "question": question.question,
        "content": question.content,
        "answers": answer_json
      })

