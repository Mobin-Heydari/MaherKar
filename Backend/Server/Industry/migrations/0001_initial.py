# Generated by Django 5.1.7 on 2025-04-09 08:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IndustryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام دسته\u200cبندی')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='اسلاگ دسته\u200cبندی')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='Industry/categories-icon/', verbose_name='آیکون')),
            ],
            options={
                'verbose_name': 'دسته\u200cبندی',
                'verbose_name_plural': 'دسته\u200cبندی\u200cها',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام صنعت')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='اسلاگ صنعت')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='Industry/industries-icon/', verbose_name='آیکون')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industries', to='Industry.industrycategory', verbose_name='دسته\u200cبندی')),
            ],
            options={
                'verbose_name': 'صنعت',
                'verbose_name_plural': 'صنایع',
                'ordering': ['name'],
            },
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
