# Generated by Django 5.1.7 on 2025-06-02 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Locations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='province',
            name='slug',
        ),
    ]
