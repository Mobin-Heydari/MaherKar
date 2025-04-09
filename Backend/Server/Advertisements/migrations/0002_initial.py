# Generated by Django 5.1.7 on 2025-04-09 08:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Advertisements', '0001_initial'),
        ('Companies', '0001_initial'),
        ('Profiles', '0001_initial'),
        ('Resumes', '0001_initial'),
        ('Subscriptions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Advertisement_Owner', to=settings.AUTH_USER_MODEL, verbose_name='مالک'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='subscription',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Advertisements_Subscription', to='Subscriptions.advertisementsubscription', verbose_name='اشتراک'),
        ),
        migrations.AddField(
            model_name='application',
            name='job_seeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Applications', to='Profiles.jobseekerprofile'),
        ),
        migrations.AddField(
            model_name='application',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Resumes.jobseekerresume'),
        ),
        migrations.AddField(
            model_name='jobadvertisement',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Job_Advertisement', to='Advertisements.advertisement', verbose_name='آگهی'),
        ),
        migrations.AddField(
            model_name='jobadvertisement',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Company_Advertisement', to='Companies.company', verbose_name='شرکت'),
        ),
        migrations.AddField(
            model_name='jobadvertisement',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Employer_Advertisement', to='Profiles.employerprofile', verbose_name='کارفرما'),
        ),
        migrations.AddField(
            model_name='application',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Applications', to='Advertisements.jobadvertisement'),
        ),
        migrations.AddField(
            model_name='resumeadvertisement',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Resume_Advertisement', to='Advertisements.advertisement', verbose_name='آگهی'),
        ),
        migrations.AddField(
            model_name='resumeadvertisement',
            name='job_seeker_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Profile', to='Profiles.jobseekerprofile', verbose_name='پروفایل کارجو'),
        ),
        migrations.AddField(
            model_name='resumeadvertisement',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Resume', to='Resumes.jobseekerresume', verbose_name='رزومه'),
        ),
    ]
