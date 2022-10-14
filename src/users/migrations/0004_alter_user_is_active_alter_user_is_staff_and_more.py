# Generated by Django 4.1 on 2022-10-14 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Inactive users can't login. Use this instead of deleting the user.",
                verbose_name="Is active",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(
                default=False,
                help_text="Only staff users can access the admin",
                verbose_name="Is staff",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(
                default=False, help_text="Super users have all permissions", verbose_name="Is admin"
            ),
        ),
    ]