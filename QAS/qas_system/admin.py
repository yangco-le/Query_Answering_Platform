from django.contrib import admin

# Register your models here.

from .models import User, Subject, Question, Comment

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Comment)