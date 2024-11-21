# Generated by Django 4.0.2 on 2023-04-30 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_remove_ticket_unique_ticket_row_seat_movie_session_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ticket',
            name='unique_ticket_row_seat',
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='unique_ticket_row_seat'),
        ),
    ]
