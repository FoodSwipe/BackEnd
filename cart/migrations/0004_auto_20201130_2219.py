# Generated by Django 3.1.3 on 2020-11-30 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
        ('cart', '0003_auto_20201130_2207'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('order', 'item')},
        ),
    ]
