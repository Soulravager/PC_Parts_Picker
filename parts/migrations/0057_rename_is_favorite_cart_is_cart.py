# Generated by Django 5.1.2 on 2025-04-01 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0056_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='is_favorite',
            new_name='is_cart',
        ),
    ]
