# Generated by Django 5.0.3 on 2024-04-12 02:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_paymentmethod_user'),
        ('products_app', '0008_alter_product_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(max_length=20)),
                ('order_status', models.CharField(max_length=20)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('review', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products_app.product')),
            ],
        ),
    ]
