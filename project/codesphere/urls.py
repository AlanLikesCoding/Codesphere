# URLS for the main pages of Codesphere, pages that are accesible to everyone, not admin panel
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.login_view, name="login"),
  path("reset", views.reset, name="reset"),
  path("reset/<uidb64>/<token>", views.reset, name="reset"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),
  path('verify/<uidb64>/<token>', views.activate, name='activate'),
  path("ask", views.ask, name="ask"),
  path("about/<int:_user>", views.about, name="about"),
  path("forum", views.forum, name="forum"),
  path("forum/<int:_sort>", views.forum, name="forum"),
  path("forum/<int:_sort>/<str:_tag>", views.forum, name="forum"),
  path("q/<int:_question>", views.display, name="display"),
  path("api/ask", views.apiask, name="apiask"),
  path("api/ans", views.apians, name="apians"),
  path("api/up/q/<int:_question>", views.apiup, name="apiup"),
  path("api/up/a/<int:_question>", views.apiaup, name="apiaup"),
  path("api/edit/q/<int:_question>", views.apiqedit, name="apiqedit"),
  path("api/comment/q/<int:_question>", views.apiqcomment, name="apiqcomment"),
  path("api/comment/a/<int:_answer>", views.apiacomment, name="apiacomment"),
  path("api/search", views.apisearch, name="apisearch")
] 
