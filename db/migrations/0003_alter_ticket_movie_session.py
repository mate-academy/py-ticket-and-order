# Generated by Django 4.0.2 on 2024-09-02 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_user_order_alter_movie_actors_alter_movie_genres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='movie_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='db.moviesession'),
        ),
    ]
