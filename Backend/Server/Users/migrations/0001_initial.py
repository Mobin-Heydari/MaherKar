# Generated by Django 5.1.7 on 2025-04-09 08:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdCardInFormation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_card_number', models.CharField(blank=True, max_length=13, null=True, verbose_name='شماره ملی')),
                ('id_card', models.FileField(blank=True, help_text='بارگذاری تصویر/اسکن کارت ملی', null=True, upload_to='Users/id_cards/', verbose_name='کارت ملی')),
                ('id_card_status', models.CharField(choices=[('P', 'در انتظار تایید'), ('V', 'تایید شده'), ('R', 'رد شده')], default='P', help_text='وضعیت بررسی کارت ملی', max_length=1, verbose_name='وضعیت کارت ملی')),
            ],
            options={
                'verbose_name': 'اطلاعات کارت ملی',
                'verbose_name_plural': 'اطلاعات کارت ملی',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_type', models.CharField(choices=[('JS', 'جوینده کار'), ('EM', 'کارفرما'), ('SU', 'پشتیبان'), ('AD', 'مدیر')], max_length=2, verbose_name='نوع کاربر')),
                ('status', models.CharField(choices=[('ACT', 'فعال'), ('SUS', 'تعلیق شده'), ('DEL', 'حذف شده')], default='ACT', max_length=3, verbose_name='وضعیت حساب کاربری')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')),
                ('username', models.CharField(max_length=40, unique=True, verbose_name='نام کاربری')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='نام و نام خوانوادگی')),
                ('joined_date', models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین به\u200cروزرسانی')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_admin', models.BooleanField(default=False, verbose_name='مدیر')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('id_card_info', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='id_card_info', to='Users.idcardinformation', verbose_name='اطلاعات کارت ملی')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ['joined_date'],
            },
        ),
    ]
