# Generated by Django 3.1.3 on 2020-12-17 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Customer Profile', 'verbose_name_plural': 'Customer Profiles'},
        ),
        migrations.AlterModelOptions(
            name='profileimage',
            options={'verbose_name': 'Customer Profile Image', 'verbose_name_plural': 'Customer Profile Images'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='contacts',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='current_city',
        ),
        migrations.AddField(
            model_name='profile',
            name='contact',
            field=models.PositiveBigIntegerField(default=9843500000, unique=True),
            preserve_default=False,
        ),
    ]
