# Generated by Django 4.2.3 on 2023-08-16 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='verified',
        ),
    ]