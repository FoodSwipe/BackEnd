# Generated by Django 3.1.4 on 2020-12-26 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20201226_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlysalesreport',
            name='count',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
