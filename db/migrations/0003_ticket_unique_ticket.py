# Generated by Django 4.0.2 on 2024-02-19 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_user_order_alter_movie_actors_alter_movie_genres_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('movie_session', 'row', 'seat'), name='unique_ticket'),
        ),
    ]
