# Generated by Django 5.0.4 on 2024-04-06 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=150)),
                ('message', models.CharField(max_length=350)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
