# Generated by Django 5.1.7 on 2025-03-19 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_type', models.CharField(choices=[('JS', 'جوینده کار'), ('EM', 'کارفرما'), ('SU', 'پشتیبان'), ('AD', 'مدیر')], max_length=2, verbose_name='نوع کاربر')),
                ('tfa_status', models.CharField(choices=[('A', 'تایید شده'), ('UA', 'تایید نشده')], default='UA', max_length=2, verbose_name='وضعیت احراز هویت دو مرحله\u200cای')),
                ('status', models.CharField(choices=[('ACT', 'فعال'), ('SUS', 'تعلیق شده'), ('DEL', 'حذف شده')], default='ACT', max_length=3, verbose_name='وضعیت حساب کاربری')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')),
                ('username', models.CharField(max_length=40, unique=True, verbose_name='نام کاربری')),
                ('joined_date', models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_admin', models.BooleanField(default=False, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ['joined_date'],
            },
        ),
    ]
