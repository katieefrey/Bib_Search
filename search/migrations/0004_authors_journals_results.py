# Generated by Django 3.0.4 on 2020-04-01 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_adstest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('jnum', models.IntegerField(default=0)),
                ('anum', models.IntegerField(default=0)),
                ('daterange', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Journals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jname', models.CharField(blank=True, max_length=250, null=True)),
                ('articlenum', models.IntegerField(default=0)),
                ('resultset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='search.Results')),
            ],
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aname', models.CharField(blank=True, max_length=250, null=True)),
                ('rart', models.IntegerField(default=0)),
                ('nrart', models.IntegerField(default=0)),
                ('rcite', models.IntegerField(default=0)),
                ('nrcite', models.IntegerField(default=0)),
                ('rfirst', models.IntegerField(default=0)),
                ('nrfirst', models.IntegerField(default=0)),
                ('resultset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='search.Results')),
            ],
        ),
    ]