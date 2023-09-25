# Generated by Django 4.0 on 2022-06-27 16:31

import django.contrib.auth.models
from django.db import migrations, models

import users.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="DjangoGroupProxy",
            fields=[],
            options={
                "verbose_name": "User Group",
                "verbose_name_plural": "User Groups",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.group",),
            managers=[
                ("objects", django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, unique=True, verbose_name="Email address"),
                ),
                ("first_name", models.CharField(max_length=30, verbose_name="First name")),
                ("last_name", models.CharField(max_length=50, verbose_name="Last name")),
                ("is_active", models.BooleanField(default=True, verbose_name="Is active")),
                ("is_staff", models.BooleanField(default=False, verbose_name="Is staff")),
                ("is_superuser", models.BooleanField(default=False, verbose_name="Is admin")),
                (
                    "date_joined",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date joined"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
            managers=[
                ("objects", users.models.UserManager()),
            ],
        ),
    ]
