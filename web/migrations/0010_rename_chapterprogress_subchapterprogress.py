# Generated by Django 4.2 on 2025-05-09 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0009_alter_chapter_modified_date_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ChapterProgress", new_name="SubChapterProgress",
        ),
    ]
