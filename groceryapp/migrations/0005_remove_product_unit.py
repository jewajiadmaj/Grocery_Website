# Generated by Django 5.0.4 on 2024-04-12 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0004_unit_product_qty_product_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='unit',
        ),
    ]
