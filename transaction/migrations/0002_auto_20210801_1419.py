# Generated by Django 3.1.4 on 2021-08-01 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-created_at']},
        ),
    ]
