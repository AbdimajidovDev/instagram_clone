from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserConfirmation
from django.utils.translation import gettext_lazy as _


class UserModelAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number')
    ordering = ('-created_time',)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone_number", "photo", "auth_type", "user_role", "auth_status")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )

admin.site.register(User, UserModelAdmin)
admin.site.register(UserConfirmation)
