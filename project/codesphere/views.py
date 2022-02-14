
# External Libaries(outside of Django)
import json
import os
# Geolocation
from json import load
from urllib.request import urlopen
# Local Libaries
from .libs import generate_token
from .libs import Colors
from .libs import Tag
from .libs import AnswerNumber
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
from .models import QuestionComment
from .models import AnswerComment

# Django Forms
from .forms import LoginForm
from .forms import RegisterForm
from .forms import AskForm
from .forms import AboutForm
from .forms import CommentForm

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

def reset(request, token = None, uidb64 = None):
  if request.method == "POST":
    if "email" in request.POST:
      if User.objects.filter(email=request.POST["email"]).first() is not None:
        user = User.objects.filter(email=request.POST["email"]).first()
        _email = request.POST["email"]
        current_site = get_current_site(request)
        mail_subject = 'Reset your password.'
        message = render_to_string('codesphere/reset_password.html', {
            'user': user,
            'domain': current_site.domain,
            'id': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })
        send_mail(mail_subject, message, 'support@codesphere.org', [_email])
        return render("reset_prompt.html", {
          "message": "Please check your email to reset your password."
        })
  else:
    return render(request, "codesphere/reset_prompt.html")

  if token is not None and uidb64 is not None:
    if request.method == "POST":
      if request.POST["password"] != request.POST["confirmation"]:
        return render("codesphere/reset.html", {
          "message": "Password and confirmation don't match!"
        })
      try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
      except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
      if user is not None and account_activation_token.check_token(user, token):
        user.passord = request.POST["password"]
        user.save()
        return HttpResponseRedirect(reverse("login"))
      else:
        return HttpResponse("codesphere/reset.html", {
          "message": "Password reset link isn't valid!"
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

def forum(request, _sort=None, _tag=None):
  # Output all questions to forum page
  data = None
  # Get the most popular posts for sidepanel
  popular = Question.objects.order_by('upvotes')[:3]
  # If sort isn't None
  if(_sort is not None):
    if _sort == 1:
      data = Question.objects.order_by('-timestamp')
      print("recent")
    elif _sort == 2:
      data = Question.objects.order_by('-upvotes')
      print("upvotes")
    elif _sort == 3:
      data = Question.objects.order_by('timestamp')
      print("oldest")
    elif _sort == 4:
      data = Question.objects.order_by('upvotes')
      print("oldest")
    else:
      data = Question.objects.all()
    # Tag list
    tag_list = []
    id_list = []
    # If tag is not None:          
    if _tag is not None:
      tags = _tag.split("|")
      for i in tags:
        if i != "":
          tag_list.append(i)
      print("tag_list", tag_list)
      for i in data:
        __tag = i.tags.split("|")
        for j in __tag:
          for x in tag_list:
            if x is None or j is None:
              break
            if x == j:
              id_list.append(i.pk)
              break
            
      data = data.filter(pk__in = id_list)
  else:
    data = Question.objects.all()
  tags = []
  # Get number of answers
  answer = []
  for i in data:
    answer_no = Answer.objects.filter(answered__id__exact=i.pk).count
    answer.append(AnswerNumber(answer_no, i.pk))
    _tags = i.tags.split("|")
    if _tags is not None:
      for j in _tags:
        tags.append(Tag(j, i.pk))
    elif i.tags is not None:
      tags.append(Tag(i.tags, i.pk))

  return render(request, "codesphere/forum.html", {
    "questions": data,
    "popular": popular,
    "answers": answer,
    "tag": tags
  })

def display(request, _question):
  # Display the question
  question = Question.objects.get(pk=_question)
  # Display all answwers with the answwered id corresponding to the questions id
  answers = Answer.objects.filter(answered__id__exact = _question)
  # Get question comments
  qcomments = QuestionComment.objects.filter(question__id__exact = _question)
  id_list = []
  for i in answers:
    append_val = AnswerComment.objects.filter(answer__id__exact = i.pk)
    if len(append_val) > 1:
      for j in append_val:
        if hasattr(j, "pk"):
          id_list.append(j.pk)
    else:
      if hasattr(append_val.first(), "pk"):
        id_list.append(append_val.first().pk)
  # Get answer comments
  acomments = AnswerComment.objects.filter(id__in=id_list)
  return render(request, "codesphere/display.html", {
    "question": question, 
    "answers": answers,
    "comment": CommentForm(),
    "ask": AskForm(initial={
      "question": question.question,
      "tags": question.tags,
      "content": question.content
    }),
    "tags": question.tags.split("|"),
    "qcomments": qcomments,
    "acomments": acomments
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
      _tags = form.cleaned_data["tags"]
      post = Question.objects.create(asker = _user, question = _question, content = _content, tags = _tags)
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

def apiqcomment(request, _question):
  url = "display";
  if(request.method == "POST"):
    _user = request.user
    form = CommentForm(request.POST)
    if form.is_valid():
      _content = form.cleaned_data["content"]
      comment = QuestionComment.objects.create(content = _content, commenter = _user, question = Question.objects.get(pk=_question))
      comment.save()
  return redirect(reverse(url, kwargs={"_question": _question}))

def apiacomment(request, _answer):
  url = "display";
  _question = Answer.objects.get(pk=_answer).answered.pk
  if(request.method == "POST"):
    _user = request.user
    form = CommentForm(request.POST)
    if form.is_valid():
      _content = form.cleaned_data["content"]
      comment = AnswerComment.objects.create(content = _content, commenter = _user, answer = Answer.objects.get(pk=_answer))
      comment.save()
  return redirect(reverse(url, kwargs={"_question": _question}))

def apiqedit(request, _question):
  _user = request.user
  id = _question
  url = "display";
  question = Question.objects.get(pk=_question)
  if request.method == "POST":
    if _user.pk == question.asker.pk:
      form = AskForm(request.POST)
      if form.is_valid():
        _question = form.cleaned_data["question"]
        _tags = form.cleaned_data["tags"]
        _content = form.cleaned_data["content"]
        question.question = _question
        question.tags = _tags
        question.content = _content
        question.save()
  return redirect(reverse(url, kwargs={"_question": id}))

def apiaedit(request, _answer):
  _user = request.user
  url = "display";
  answer = Answer.objects.get(pk=_answer)
  id = answer.answered.pk
  if request.method == "POST":
    if _user.pk == answer.replier.pk:
      _content = request.POST["content"]
      answer.content = _content
      answer.save()
  return redirect(reverse(url, kwargs={"_question": id}))

def apicorrect(request, _answer, _bool):
  _user = request.user
  answer = Answer.objects.get(pk=_answer)
  question = answer.answered
  id = question.pk
  url = "display"
  if request.method == "POST":
    if request.user.pk == question.asker.pk:
      question.answered_correct = _bool
      answer.correct = _bool
      answer.save()
      question.save()

  return redirect(reverse(url, kwargs={"_question": id}))