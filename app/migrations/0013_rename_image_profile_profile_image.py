# Generated by Django 4.1.6 on 2023-02-20 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='profile_image',
        ),
    ]