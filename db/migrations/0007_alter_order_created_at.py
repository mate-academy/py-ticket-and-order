# Generated by Django 4.0.2 on 2025-01-15 19:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_alter_order_options_alter_ticket_row_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
