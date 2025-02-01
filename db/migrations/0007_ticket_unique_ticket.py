# Generated by Django 4.0.2 on 2025-01-31 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_alter_order_options_ticket'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='unique_ticket'),
        ),
    ]
