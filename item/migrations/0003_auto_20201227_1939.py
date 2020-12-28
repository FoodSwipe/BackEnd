# Generated by Django 3.1.4 on 2020-12-27 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_topandrecommendeditem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topandrecommendeditem',
            options={'verbose_name': 'Top and Recommended Item', 'verbose_name_plural': 'Top and Recommended Items'},
        ),
        migrations.AlterField(
            model_name='topandrecommendeditem',
            name='menu_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='special', to='item.menuitem'),
        ),
    ]