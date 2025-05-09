# Generated by Django 5.1.7 on 2025-04-09 08:37

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Advertisements', '0001_initial'),
        ('Subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionOrder',
            fields=[
                ('payment_status', models.CharField(choices=[('pending', 'در انتظار'), ('paid', 'پرداخت شده'), ('canceled', 'لغو شده'), ('failed', 'ناموفق')], default='pending', max_length=20, verbose_name='وضعیت پرداخت')),
                ('durations', models.IntegerField(default=1, verbose_name='مدت زمان اشتراک')),
                ('price', models.IntegerField(default=0, verbose_name='قیمت')),
                ('total_price', models.IntegerField(verbose_name='قیمت نهایی')),
                ('order_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='آیدی')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Advertisements.advertisement', verbose_name='آگهی')),
                ('advertisement_subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Subscriptions.advertisementsubscription', verbose_name='اشتراک آگهی ها')),
            ],
            options={
                'verbose_name': 'سفارش آگهی',
                'verbose_name_plural': 'سفارشات آگهی ها',
            },
        ),
    ]
