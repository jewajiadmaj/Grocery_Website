# Generated by Django 5.0.4 on 2024-04-22 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0011_alter_customer_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer_id', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('mobile_number', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('product_id', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=200)),
                ('quantity', models.CharField(max_length=200)),
                ('product_sub_price', models.CharField(max_length=200)),
                ('product_total', models.CharField(max_length=200)),
            ],
        ),
    ]
