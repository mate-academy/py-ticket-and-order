# Generated by Django 4.0.2 on 2022-10-26 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_user_order_ticket_alter_movie_title_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='movie',
            name='db_movie_title_5d0841_idx',
        ),
    ]
