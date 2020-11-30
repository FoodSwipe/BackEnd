# Generated by Django 3.1.3 on 2020-11-30 15:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import item_group.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItemGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(max_length=512)),
                ('price', models.DecimalField(blank=True, decimal_places=2, help_text='in Rupees', max_digits=8, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, help_text='in %', max_digits=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='MenuItemGroupCreator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='MenuItemGroupModifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Menu Item Group',
                'verbose_name_plural': 'Menu Item Groups',
            },
        ),
        migrations.CreateModel(
            name='MenuItemGroupImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=item_group.models.upload_menu_item_group_media_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG', 'webp'])])),
                ('menu_item_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RelMenuItemForImage', to='item_group.menuitemgroup')),
            ],
            options={
                'verbose_name': 'Menu Item Group Image',
                'verbose_name_plural': 'Menu Item Group Images',
            },
        ),
    ]
