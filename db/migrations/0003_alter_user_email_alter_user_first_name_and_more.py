# Generated by Django 4.0.2 on 2025-02-19 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_user_order_alter_movie_actors_alter_movie_genres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
