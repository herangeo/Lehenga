# Generated by Django 5.0.4 on 2024-10-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_4',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_5',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]