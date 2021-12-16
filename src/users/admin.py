from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import MyUserCreationForm, MyUserChangeForm
from .models import ProxyUser
from rest_framework.authtoken.models import TokenProxy
from rest_framework.authtoken.admin import TokenAdmin


class UserAdmin(DjangoUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    icon_name = "person"

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
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
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
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    readonly_fields = ("date_joined",)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")


class MyTokenAdmin(TokenAdmin):
    icon_name = "https"


admin.site.register(ProxyUser, UserAdmin)
admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, MyTokenAdmin)
