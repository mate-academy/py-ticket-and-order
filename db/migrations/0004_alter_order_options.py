# Generated by Django 4.0.2 on 2025-03-02 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
    ]
