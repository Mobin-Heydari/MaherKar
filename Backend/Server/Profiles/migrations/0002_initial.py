# Generated by Django 5.1.7 on 2025-03-22 14:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Locations', '0001_initial'),
        ('Profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Locations.city', verbose_name='مکان'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='experience',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_locations', to='Locations.city', verbose_name='مکان'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='id_card_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_id_card_info', to='Profiles.idcardinformation', verbose_name='اطلاعات کارت ملی'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='id_card_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_id_card_info', to='Profiles.idcardinformation', verbose_name='اطلاعات کارت ملی'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Locations.city', verbose_name='شهر'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='experience',
            name='job_seeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='Profiles.jobseekerprofile', verbose_name='جوینده کار'),
        ),
        migrations.AddField(
            model_name='education',
            name='job_seeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='Profiles.jobseekerprofile', verbose_name='جوینده کار'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='personal_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_personal_info', to='Profiles.personalinformation', verbose_name='اطلاعات شخصی'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='personal_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_personal_info', to='Profiles.personalinformation', verbose_name='اطلاعات شخصی'),
        ),
        migrations.AddField(
            model_name='skill',
            name='category',
            field=models.ForeignKey(blank=True, help_text='انتخاب دسته\u200cبندی مهارت (اختیاری)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Profiles.skillcategory', verbose_name='دسته\u200cبندی'),
        ),
        migrations.AddField(
            model_name='supportprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
