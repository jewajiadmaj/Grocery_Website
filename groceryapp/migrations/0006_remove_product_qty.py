# Generated by Django 5.0.4 on 2024-04-12 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0005_remove_product_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='qty',
        ),
    ]