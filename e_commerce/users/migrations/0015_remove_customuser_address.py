# Generated by Django 5.0.3 on 2024-04-11 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_customuser_address_alter_customuser_pincode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
    ]
