# Generated by Django 5.0.7 on 2024-08-19 16:08

import base.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_productimage_features_alter_category_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethod',
            name='card_number',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='expiry_date',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='payment_type',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='provider',
        ),
        migrations.CreateModel(
            name='BankInformation',
            fields=[
                ('id', models.UUIDField(default=base.models.generate_uuid, editable=False, primary_key=True, serialize=False)),
                ('acc_holder_name', models.CharField(max_length=255)),
                ('acc_number', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=255)),
                ('routing_number', models.CharField(max_length=10)),
                ('iban', models.CharField(max_length=10)),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.paymenttype')),
            ],
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='provider_bank',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.bankinformation'),
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.UUIDField(default=base.models.generate_uuid, editable=False, primary_key=True, serialize=False)),
                ('card_holder_name', models.CharField(max_length=255)),
                ('card_number', models.CharField(max_length=255)),
                ('expired_date', models.DateField()),
                ('cvv', models.CharField(max_length=10)),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.paymenttype')),
            ],
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='provider_card',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.creditcard'),
        ),
    ]
