# Generated by Django 5.1.5 on 2025-01-15 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0002_alter_movie_actors_alter_movie_genres_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["-created_at"]},
        ),
    ]
