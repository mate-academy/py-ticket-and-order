# Generated by Django 4.0.2 on 2024-09-30 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_alter_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
