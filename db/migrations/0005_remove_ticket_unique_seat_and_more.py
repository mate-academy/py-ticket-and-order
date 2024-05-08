# Generated by Django 4.0.2 on 2024-05-08 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ticket',
            name='unique_seat',
        ),
        migrations.RemoveIndex(
            model_name='movie',
            name='db_movie_title_5d0841_idx',
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='movie_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.moviesession'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.order'),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='unique_seat_for_movie_session'),
        ),
    ]
