# Generated by Django 4.0.2 on 2023-01-22 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_created=True, auto_now_add=True),
        ),
    ]
