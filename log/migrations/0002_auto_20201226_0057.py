# Generated by Django 3.1.4 on 2020-12-26 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='log_mode',
            new_name='mode',
        ),
    ]