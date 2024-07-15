# Generated by Django 5.0.6 on 2024-07-12 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_store_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.stock'),
        ),
    ]
