# Generated by Django 3.0.4 on 2020-04-01 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200401_1149'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('search', '0004_authors_journals_results'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bibgroup',
        ),
        migrations.AddField(
            model_name='results',
            name='username',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]