# Generated by Django 5.1.7 on 2025-03-24 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertisements', '0001_initial'),
        ('Profiles', '0005_remove_experience_job_seeker_and_more'),
        ('Resumes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'در انتظار'), ('in_review', 'در حال بررسی'), ('accepted', 'پذیرفته شده'), ('rejected', 'رد شده')], default='pending', max_length=20)),
                ('employer_notes', models.TextField(blank=True, null=True)),
                ('viewed_by_employer', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='Advertisements.jobadvertisement')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='Profiles.jobseekerprofile')),
                ('resume', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Resumes.jobseekerresume')),
            ],
        ),
    ]
