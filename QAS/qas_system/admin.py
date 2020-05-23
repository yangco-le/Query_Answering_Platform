from django.contrib import admin
from .models import User, Subject, Question, Comment, Tipoff


admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Tipoff)
