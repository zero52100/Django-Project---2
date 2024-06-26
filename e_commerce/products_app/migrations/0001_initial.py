# Generated by Django 5.0.3 on 2024-04-09 11:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='products_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thumbnail', models.ImageField(upload_to='thumbnails/')),
                ('available_quantity', models.PositiveIntegerField()),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight_unit', models.CharField(choices=[('kg', 'Kilogram'), ('g', 'Gram'), ('ml', 'Milliliter'), ('l', 'Liter'), ('pcs', 'Pieces')], default='kg', max_length=10)),
                ('veg_non_veg', models.CharField(choices=[('vegetarian', 'Vegetarian'), ('non_vegetarian', 'Non-Vegetarian')], max_length=15)),
                ('expiry_date', models.DateField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(related_name='products', to='products_app.productimage'),
        ),
    ]
