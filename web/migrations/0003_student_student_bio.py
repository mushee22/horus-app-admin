# Generated by Django 4.2 on 2025-04-30 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0002_course_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="student_bio",
            field=models.TextField(blank=True, null=True),
        ),
    ]
