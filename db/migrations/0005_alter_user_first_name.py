# Generated by Django 4.0.2 on 2023-07-13 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_alter_order_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
