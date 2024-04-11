# Generated by Django 5.0.3 on 2024-04-09 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0002_rename_name_product_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('staples', 'Vegetarian'), ('snacks_&_beverages', 'Snacks and Beverages'), ('household_items', 'Household Items'), ('dairy_and_eggs', 'Dairy and Eggs')], max_length=55),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]