# Generated by Django 4.2 on 2023-05-02 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='package',
            name='gig',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='portfolio.gig'),
        ),
        migrations.AddField(
            model_name='gig',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gigs', to='portfolio.portfolio'),
        ),
        migrations.AlterUniqueTogether(
            name='package',
            unique_together={('gig', 'package_type')},
        ),
    ]
