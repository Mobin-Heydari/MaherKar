# Generated by Django 5.1.7 on 2025-04-04 09:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0002_subscriptionorder_durations_subscriptionorder_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionorder',
            name='order_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='آیدی'),
        ),
    ]
