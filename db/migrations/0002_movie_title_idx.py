# Generated by Django 4.0.2 on 2023-09-08 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['title'], name='title_idx'),
        ),
    ]
