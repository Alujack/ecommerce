# Generated by Django 5.0.7 on 2024-08-27 02:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_favourite_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='line_total',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='order_total',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.address'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('delivered', 'Delivered'), ('canceled', 'Canceled'), ('refunded', 'Refunded')], default='pending', max_length=255),
        ),
    ]
