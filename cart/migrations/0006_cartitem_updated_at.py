# Generated by Django 3.1.3 on 2020-12-01 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20201130_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
