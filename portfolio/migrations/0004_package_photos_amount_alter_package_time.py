# Generated by Django 4.2 on 2023-06-07 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20230505_0546'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='photos_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]