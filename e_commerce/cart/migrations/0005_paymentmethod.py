# Generated by Django 5.0.3 on 2024-04-12 02:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cart_total_cart_value_alter_cartitem_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('debit_card', 'Debit Card'), ('upi', 'UPI')], max_length=20)),
                ('card_number', models.CharField(blank=True, max_length=16, null=True)),
                ('cvv', models.CharField(blank=True, max_length=4, null=True)),
                ('expiry_date', models.CharField(blank=True, max_length=7, null=True)),
                ('upi_id', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]