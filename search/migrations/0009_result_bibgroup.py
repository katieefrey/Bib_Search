# Generated by Django 3.0.4 on 2020-04-01 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200401_1149'),
        ('search', '0008_result_namelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='bibgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Bibgroup'),
        ),
    ]
