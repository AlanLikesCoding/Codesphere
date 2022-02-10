from django.contrib import admin
from codesphere import models

# Adding extra funcionality to Django Admin

admin.site.site_header  =  "Codesphere Admin"  
admin.site.site_title  =  "Codesphere Admin"
admin.site.index_title  =  "Codesphere Admin"

class AnswerInline(admin.TabularInline):
  model = models.Answer

class UserAdmin(admin.ModelAdmin):
  list_display = ["username", "date_joined", "reputation"]
  list_filter = ["date_joined"]
  search_fields = ["username", "email", "reputation"]

class QuestionAdmin(admin.ModelAdmin):
  inlines = [AnswerInline,]
  list_display = ["get_user", "question", "upvotes", "answered_correct"]
  ordering = ["upvotes"]
  search_fields =  ["question"]
  def get_user(self, obj):
        return obj.asker.username

class AnswerAdmin(admin.ModelAdmin):
  list_display = ["get_user", "upvotes", "content"]
  ordering = ["upvotes"]
  def get_user(self, obj):
      return obj.replier.username

# Register your models here.
# User models
admin.site.register(models.User, UserAdmin)
# Question models
admin.site.register(models.Question, QuestionAdmin)
# Answer models
admin.site.register(models.Answer, AnswerAdmin)
# Comment models
# Question
admin.site.register(models.QuestionComment)
# Answer
admin.site.register(models.AnswerComment)