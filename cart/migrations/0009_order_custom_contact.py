# Generated by Django 3.1.3 on 2020-12-20 15:08

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_auto_20201220_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='custom_contact',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
