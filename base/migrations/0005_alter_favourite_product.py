# Generated by Django 5.0.7 on 2024-08-22 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_storecategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favourite',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.product'),
        ),
    ]