# Generated by Django 3.1.4 on 2021-08-01 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_group', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitemgroup',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Menu Item Group', 'verbose_name_plural': 'Menu Item Groups'},
        ),
    ]
