# Generated by Django 3.1.4 on 2023-04-10 10:56

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import item_group.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MenuItemGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=512, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        upload_to=item_group.models.upload_menu_item_group_media_to,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                [
                                    "png",
                                    "jpg",
                                    "jpeg",
                                    "gif",
                                    "bmp",
                                    "tiff",
                                    "JPG",
                                    "webp",
                                ]
                            )
                        ],
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="MenuItemGroupCreator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="MenuItemGroupModifier",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Menu Item Group",
                "verbose_name_plural": "Menu Item Groups",
                "ordering": ["-updated_at"],
            },
        ),
    ]
