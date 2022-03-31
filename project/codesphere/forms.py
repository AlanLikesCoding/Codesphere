from django import forms
from . import models

# Form on /login.html page

class LoginForm(forms.Form):
  # Login Username
  username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your username here...", "class":"form-control", "id":"user", "name":"username"}))
  # Login passcode
  password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter your passcode here...", "class":"form-control", "id":"password", "name":"password"}), max_length=50)

# Form on the /register.html page
class RegisterForm(forms.Form):
  class Meta:
    model = models.User
  # Login username
  username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your username here...", "class":"form-control", "id":"user", "name":"username"}))
  # Login email
  email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Enter your contact email here...", "class":"form-control", "id":"email", "name":"email"}), max_length=254)
  # Login passcode
  password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter your passcode here...", "class":"form-control", "id":"password", "name":"password"}), max_length=50)
  # Verify passcode
  confirmation = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm your passcode here...", "class":"form-control", "id":"confirmation", "name":"confirmation"}), max_length=50)

# Form on the /ask.html page
class AskForm(forms.Form):
  class Meta: 
    model = models.Question
  # Question header form
  question = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your question here...", "id":"header",}),max_length=130, min_length=10)
  tags = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Please enter your tags here...", "id":"tags_input", "type": "hidden"}),max_length=130, min_length=10)
  # Question content form
  content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter information about your question that will help others answer your question here...","class":"form-control", "rows": 12}), min_length=40)

  # Form on the /ask.html page
class CollectiveForm(forms.Form):
  class Meta: 
    model = models.Collective
  # Collective name
  name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter the name of your collective here...","id":"header"}), max_length=20)
  # Collective description
  content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter information about your collective here...","class":"form-control", "rows": 12}), max_length=100)  
  # Collective icon
  icon = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={"name": "icon"}))

class AboutForm(forms.Form):
  class Meta:
    model = models.User
  # Bio form
  bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"placeholder": "Talk about yourself for others to know you better...", "rows": 12}))
  upload = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={"name": "upload"}))

class CommentForm(forms.Form):
  content = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your comment here...","class":"form-control", "rows": 12}))