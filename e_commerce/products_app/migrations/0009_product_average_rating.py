# Generated by Django 5.0.3 on 2024-04-12 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0008_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='average_rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
