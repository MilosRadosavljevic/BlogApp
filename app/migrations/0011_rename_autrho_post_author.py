# Generated by Django 4.1.6 on 2023-02-20 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_post_autrho'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='autrho',
            new_name='author',
        ),
    ]
