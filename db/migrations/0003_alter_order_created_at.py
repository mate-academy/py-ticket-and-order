# Generated by Django 4.0.2 on 2023-09-09 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_user_order_ticket_movie_db_movie_title_5d0841_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
