# Generated by Django 5.1.2 on 2024-11-07 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('CPU', 'CPU'), ('Motherboard', 'Motherboard'), ('RAM', 'RAM'), ('GPU', 'GPU'), ('SSD', 'SSD'), ('PSU', 'PSU')], max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.CharField(max_length=200)),
                ('compatibility', models.JSONField()),
            ],
        ),
    ]
