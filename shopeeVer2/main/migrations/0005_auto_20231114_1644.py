# Generated by Django 3.1.6 on 2023-11-14 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Số điện thoại không hợp lệ', regex='^0\\d{9}$')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_no',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(),
        ),
    ]
