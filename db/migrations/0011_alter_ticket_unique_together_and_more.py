# Generated by Django 4.0.2 on 2024-09-16 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_alter_ticket_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='unique_seat_row_session'),
        ),
    ]
