# Generated by Django 5.0.3 on 2024-04-10 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0006_alter_product_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='media/product_images/'),
        ),
    ]
