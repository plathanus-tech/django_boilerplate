# Generated by Django 4.2 on 2023-10-17 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="language_code",
            field=models.CharField(
                choices=[("pt-br", "Brazilian Portuguese"), ("en-us", "English")],
                default="pt-br",
                max_length=8,
                verbose_name="preference language",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="time_zone",
            field=models.CharField(
                choices=[
                    ("America/Sao_Paulo", "São Paulo - Brazil (-03:00)"),
                    ("UTC", "Universal Coordinated Time"),
                ],
                default="America/Sao_Paulo",
                max_length=32,
                verbose_name="preference time zone",
            ),
        ),
    ]
