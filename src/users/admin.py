from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy

from .forms import UserChangeForm, UserCreationForm
from .models import Group, User

admin.site.unregister(TokenProxy)
admin.site.unregister(DjangoGroup)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "email",
        "full_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_superuser", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password", "full_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    ("is_superuser", "is_staff", "is_active"),
                    ("groups",),
                    ("user_permissions",),
                )
            },
        ),
        (_("Metadata"), {"fields": ("date_joined", "last_login")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    readonly_fields = ("date_joined",)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    pass
