from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserConfirmation


class UserModelAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number')
    ordering = ('-created_time',)

admin.site.register(User, UserModelAdmin)
admin.site.register(UserConfirmation)
