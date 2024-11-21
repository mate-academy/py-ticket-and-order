# Generated by Django 4.0.2 on 2024-05-06 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_user_order_alter_movie_actors_alter_movie_genres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['title'], name='db_movie_title_5d0841_idx'),
        ),
    ]
