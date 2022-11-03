from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, GameMode, GameTitle, Score

admin.site.register(User, UserAdmin)
admin.site.register([GameMode, GameTitle, Score, ])
