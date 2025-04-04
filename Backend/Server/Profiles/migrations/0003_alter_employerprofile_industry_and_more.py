# Generated by Django 5.1.7 on 2025-03-23 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Industry', '0001_initial'),
        ('Profiles', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerprofile',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Industry.industry', verbose_name='صنعت'),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Industry.industry', verbose_name='صنعت'),
        ),
    ]
