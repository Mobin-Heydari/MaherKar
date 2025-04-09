# Generated by Django 5.1.7 on 2025-04-09 08:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Companies', '0001_initial'),
        ('Industry', '0001_initial'),
        ('Locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مدیرعامل'),
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Industry.industry', verbose_name='صنعت'),
        ),
        migrations.AddField(
            model_name='company',
            name='location',
            field=models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to='Locations.city', verbose_name='شهر'),
        ),
    ]
