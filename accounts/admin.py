from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from problems.models import Problem
from .models import User

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'subject', 'topic', 'difficulty', 'author')


admin.site.register(User, UserAdmin)


admin.site.register(Problem)