# Generated by Django 4.2 on 2023-06-08 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_package_photos_amount_alter_package_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
