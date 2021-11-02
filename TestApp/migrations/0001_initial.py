# Generated by Django 3.2.6 on 2021-10-27 16:58

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=300)),
                ('Price', models.PositiveIntegerField(default=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=90)),
                ('last_name', models.CharField(max_length=90)),
                ('email', models.EmailField(max_length=254)),
                ('complaint', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('username', models.CharField(max_length=80, unique=True)),
                ('id', models.CharField(max_length=80, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('ref', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('verified', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('address', models.TextField(max_length=2000)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('Phone_Number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('Sender_Address', models.CharField(blank=True, max_length=1000, null=True)),
                ('recipent_first_name', models.CharField(max_length=80)),
                ('recipent_last_name', models.CharField(max_length=80)),
                ('recipent_phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('Address', models.TextField(max_length=1000, verbose_name='Recipent Address')),
                ('status', models.CharField(choices=[('Not_Assigned', 'Not_Assigned'), ('Assigned', 'Assigned'), ('Delivered', 'Delivered')], default='Not_Assigned', max_length=20)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('receiver_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_city', to='TestApp.city')),
                ('sender_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_city', to='TestApp.city')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_first_name', models.CharField(max_length=80)),
                ('receiver_last_name', models.CharField(max_length=80)),
                ('receiver_phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestApp.mail')),
            ],
        ),
        migrations.CreateModel(
            name='AssignMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('Assigned', 'Assigned'), ('Delivered', 'Delivered')], default='Assigned', max_length=20)),
                ('mailid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestApp.mail')),
                ('riderid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestApp.dispatch')),
            ],
        ),
    ]