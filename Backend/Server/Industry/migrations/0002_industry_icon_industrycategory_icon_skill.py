# Generated by Django 5.1.7 on 2025-03-23 21:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Industry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='industry',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='Industry/industries-icon/', verbose_name='آیکون'),
        ),
        migrations.AddField(
            model_name='industrycategory',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='Industry/categories-icon/', verbose_name='آیکون'),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='Industry/skills-icons/', verbose_name='آیکون')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Industry.industry', verbose_name='صنعت')),
            ],
            options={
                'verbose_name': 'مهارت',
                'verbose_name_plural': 'مهارت\u200cها',
                'ordering': ['name'],
            },
        ),
    ]
