# Generated by Django 5.1.2 on 2025-03-26 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0047_motherboard_description_psu_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
        ),
    ]
