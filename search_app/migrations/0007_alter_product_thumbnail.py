# Generated by Django 5.1.3 on 2024-11-16 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0006_product_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]
