from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from problems.models import Problem, ProblemCategory
from .models import User



admin.site.register(User, UserAdmin)


admin.site.register(Problem)
admin.site.register(ProblemCategory)