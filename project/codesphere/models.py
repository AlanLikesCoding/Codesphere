from django.contrib.auth.models import AbstractUser
from django.db import models

from django.urls import reverse

# Model for user
class User(AbstractUser):
  # Many to many field for the questions that have been upvoted
  upvoted = models.ManyToManyField("Question", related_name="up", blank=True)
  # Many to many field for questions downvoted
  downvoted = models.ManyToManyField("Question", related_name = "down", blank=True)
  # Same as above
  answer_upvoted = models.ManyToManyField("Answer", related_name="a_up", blank=True)
  answer_downvoted = models.ManyToManyField("Answer", related_name="a_down", blank=True)
  # About the User
  # Profile Picture field
  picture = models.ImageField(upload_to="profile/", default="profile/default.png")
  # Text Field for Bio
  bio = models.TextField(null=True)
  # Positive int field for reputation
  reputation = models.PositiveIntegerField(default=1)


# Model for a question    
class Question(models.Model):
  # Foreign key for asker. If asker user model gets deleted, it gets set to null, and deleted_name gets set to the asker's username.
  asker = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="questions", null=True)

  deleted_name = models.TextField(null=True)

  # Timestamp of last time the model has been edited
  timestamp = models.DateTimeField(auto_now=True)

  question = models.CharField(max_length=200)
  content = models.TextField()

  # Number of upvotes a question has
  upvotes = models.IntegerField(default=0)

  # True if the asker has marked an answer as correct.
  answered_correct = models.BooleanField(default=False)

  def get_absolute_url(self):
    # In templates can call {{ question.get_absolute_url }} to get the url of this question rather than using {% url %}
    return reverse('display', kwargs={'_question' : self.pk})
  
  def serialize(self):
    pass

# Model for an answer
class Answer(models.Model):
  # Same as for Question model
  replier = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name="answers")
  
  deleted_name = models.TextField(null=True)

  # Timestamp of last time the model has been edited
  timestamp = models.DateTimeField(auto_now=True)

  content = models.TextField()
  upvotes = models.IntegerField(default=0)

  # True if asker has marked this answer as correct
  correct = models.BooleanField(default=False)

  # Foreign key for which question this answer answers
  answered = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")