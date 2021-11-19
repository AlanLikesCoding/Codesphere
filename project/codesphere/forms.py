from django import forms
from . import models
# Form on the /ask.html page
class AskForm(forms.Form):
  class Meta: 
    model = models.Question
  # Question header form
  question = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your question here...", "id":"header",}),max_length=130, min_length=10)
  # Question content form
  content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter information about your question that will help others answer your question here...","class":"form-control", "rows":12}), min_length=40)

class RegisterForm(forms.Form):
  class Meta:
    model = models.User
  # Login username
  username = forms.CharField(widget.forms.TextInput(attrs={"placeholder":"Enter your username here...", "class":"form-control", "id":"user", "name":"username"}))
  # Login email
  email = forms.CharField(widget.forms.EmailField(attrs={"placeholder":"Enter your contact email here...", "class":"form-control", "id":"email", "name":"email"}))
  # Login passcode
  password = forms.CharField(widget.forms.PasswordInput(attrs={"placeholder":"Enter your passcode here...", "class":"form-control", "id":"password", "name":"password"}))
  # Verify passcode
  confirmation = forms.CharField(widget.forms.PasswordInput(attrs={"placeholder":"Confirm your passcode here...", "class":"form-control", "id":"password", "name":"password"}))