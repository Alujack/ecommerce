# Generated by Django 5.0.7 on 2024-09-03 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_coupon_shoporder_discount_amount_shoporder_coupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='customerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.shoporder')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.store')),
            ],
        ),
    ]
