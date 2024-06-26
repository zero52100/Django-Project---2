# Generated by Django 5.0.3 on 2024-04-10 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0004_remove_product_veg_non_veg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight_unit',
            field=models.CharField(choices=[('kg', 'Kilogram'), ('g', 'Gram'), ('ml', 'Milliliter'), ('L', 'Liter'), ('pcs', 'Pieces')], default='kg', max_length=10),
        ),
    ]
