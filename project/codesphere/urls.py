# URLS for the main pages of Codesphere, pages that are accesible to everyone, not admin panel
from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),
  path("ask", views.ask, name="ask"),
  path("forum", views.forum, name="forum"),
  path("q/<int:_question>", views.display, name="display"),
  path("api/ask", views.apiask, name="apiask"),
  path("api/ans", views.apians, name="apians"),
  path("api/up/q/<int:_question>", views.apiup, name="apiup"),
  path("api/up/a/<int:_question>", views.apiaup, name="apiaup"),
]
