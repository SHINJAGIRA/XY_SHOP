# Generated by Django 5.1.3 on 2024-11-11 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_productin_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productout',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productin'),
        ),
    ]
