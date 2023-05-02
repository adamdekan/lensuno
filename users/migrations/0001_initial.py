# Generated by Django 4.2 on 2023-05-02 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import places.fields
import shortuuid.django_fields
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=9, max_length=9, prefix='', primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('is_freelancer', models.BooleanField(default=False)),
                ('bio', models.TextField(blank=True, max_length=250)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('avatar', models.ImageField(default='default.jpg', upload_to=users.models.upload_location)),
                ('location', places.fields.PlacesField(max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_flagged', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_comments', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]