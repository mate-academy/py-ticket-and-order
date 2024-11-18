# Generated by Django 5.1.1 on 2024-09-07 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ticket',
            name='unique_seat_in_session',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='row',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seat',
            field=models.IntegerField(),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('movie_session', 'order', 'row', 'seat'), name='unique_ticket'),
        ),
    ]
