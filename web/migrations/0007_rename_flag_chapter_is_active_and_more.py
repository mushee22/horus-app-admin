# Generated by Django 4.2 on 2025-05-04 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0006_package_alter_course_tutor_purchase_package"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chapter", old_name="flag", new_name="is_active",
        ),
        migrations.RenameField(
            model_name="course", old_name="flag", new_name="is_active",
        ),
        migrations.RenameField(
            model_name="package", old_name="flag", new_name="is_active",
        ),
        migrations.RenameField(
            model_name="package", old_name="name", new_name="title",
        ),
        migrations.RenameField(
            model_name="purchase", old_name="flag", new_name="is_active",
        ),
        migrations.RenameField(
            model_name="student", old_name="flag", new_name="is_active",
        ),
        migrations.RenameField(
            model_name="subchapters", old_name="flag", new_name="is_active",
        ),
        migrations.RenameField(
            model_name="tutor", old_name="flag", new_name="is_active",
        ),
        migrations.RemoveField(model_name="course", name="offer",),
        migrations.RemoveField(model_name="course", name="price",),
        migrations.RemoveField(model_name="purchase", name="course_name",),
        migrations.AddField(
            model_name="chapter",
            name="thumbnail",
            field=models.ImageField(default=1, upload_to="courses/chapters"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="package", name="offer", field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="package", name="price", field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="package",
            name="thumbnail",
            field=models.ImageField(default=1, upload_to="packages"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="chapter",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_chapter",
                to="web.course",
            ),
        ),
        migrations.AlterField(
            model_name="subchapters",
            name="thumbnail",
            field=models.ImageField(upload_to="courses/chapters/subchapters"),
        ),
    ]
