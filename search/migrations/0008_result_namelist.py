# Generated by Django 3.0.4 on 2020-04-01 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0007_delete_adstest'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='namelist',
            field=models.TextField(blank=True, null=True),
        ),
    ]
