# Generated by Django 4.0.2 on 2023-03-24 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_user_order_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='unique_ticket'),
        ),
    ]
