# Generated by Django 4.2 on 2025-05-09 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0018_remove_subchapters_is_completed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="package",
            name="features",
            field=models.ManyToManyField(
                related_name="package_features", to="web.features"
            ),
        ),
    ]
