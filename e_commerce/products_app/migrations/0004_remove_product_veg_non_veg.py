# Generated by Django 5.0.3 on 2024-04-09 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0003_alter_product_category_delete_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='veg_non_veg',
        ),
    ]
