# Generated by Django 4.0.2 on 2025-01-30 00:27

from django.db import migrations, models
from datetime import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_alter_order_options_alter_movie_actors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.utcnow),
        ),
    ]