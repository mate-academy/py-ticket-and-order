# Generated by Django 4.0.2 on 2024-05-05 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_alter_user_last_login_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
