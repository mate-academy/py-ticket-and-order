# Generated by Django 4.2.18 on 2025-01-28 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_alter_movie_actors_alter_movie_genres_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['title'], name='db_movie_title_5d0841_idx'),
        ),
    ]
