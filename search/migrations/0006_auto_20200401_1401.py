# Generated by Django 3.0.4 on 2020-04-01 18:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('search', '0005_auto_20200401_1149'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Authors',
            new_name='Author',
        ),
        migrations.RenameModel(
            old_name='Journals',
            new_name='Journal',
        ),
        migrations.RenameModel(
            old_name='Results',
            new_name='Result',
        ),
    ]
