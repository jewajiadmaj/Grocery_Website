# Generated by Django 5.0.4 on 2024-04-12 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceryapp', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]