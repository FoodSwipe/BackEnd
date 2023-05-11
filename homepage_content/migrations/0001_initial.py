# Generated by Django 3.1.4 on 2023-04-10 10:56

import django.core.validators
from django.db import migrations, models

import homepage_content.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HomePageContent",
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
                ("heading", models.CharField(max_length=255)),
                ("subtitle", models.CharField(max_length=512)),
                (
                    "image",
                    models.ImageField(
                        upload_to=homepage_content.models.upload_image_to,
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
                ("button_text", models.CharField(max_length=64)),
                ("button_icon", models.CharField(max_length=64)),
                ("button_to", models.CharField(max_length=64)),
                ("created_at", models.DateField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
