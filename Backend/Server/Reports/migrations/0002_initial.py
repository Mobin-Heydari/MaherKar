# Generated by Django 5.1.7 on 2025-04-09 08:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Profiles', '0002_initial'),
        ('Reports', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisementreport',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisement_reports', to=settings.AUTH_USER_MODEL, verbose_name='گزارش\u200cدهنده'),
        ),
        migrations.AddField(
            model_name='employerreport',
            name='reported_employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employer_reports_against', to='Profiles.employerprofile', verbose_name='کارفرمای گزارش شده'),
        ),
        migrations.AddField(
            model_name='employerreport',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employer_reports', to=settings.AUTH_USER_MODEL, verbose_name='گزارش\u200c دهنده'),
        ),
        migrations.AddField(
            model_name='jobseekerreport',
            name='reported_jobseeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_reports_against', to='Profiles.jobseekerprofile', verbose_name='جوینده کار گزارش شده'),
        ),
        migrations.AddField(
            model_name='jobseekerreport',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_reports', to=settings.AUTH_USER_MODEL, verbose_name='گزارش\u200cدهنده'),
        ),
        migrations.AddField(
            model_name='jobseekerreport',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reports.reportcategory', verbose_name='دسته\u200cبندی گزارش'),
        ),
        migrations.AddField(
            model_name='employerreport',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reports.reportcategory', verbose_name='دسته\u200cبندی گزارش'),
        ),
        migrations.AddField(
            model_name='advertisementreport',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reports.reportcategory', verbose_name='دسته\u200cبندی گزارش'),
        ),
    ]
