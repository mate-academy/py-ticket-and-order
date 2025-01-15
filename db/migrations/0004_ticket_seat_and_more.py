# Generated by Django 4.0.2 on 2025-01-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_user_order_alter_movie_title_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='seat',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='unique_row_seat_movie_session_constraint'),
        ),
    ]
