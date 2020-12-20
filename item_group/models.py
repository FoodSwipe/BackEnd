import os
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


def upload_menu_item_group_media_to(instance, filename):
    item_name = instance.name
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'menu_item_group/{item_name}/{filename}'


class MenuItemGroup(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=512, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        editable=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="MenuItemGroupCreator"
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(
        get_user_model(),
        editable=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="MenuItemGroupModifier"
    )
    image = models.ImageField(
        upload_to=upload_menu_item_group_media_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )

    class Meta:
        verbose_name = "Menu Item Group"
        verbose_name_plural = "Menu Item Groups"

    def __str__(self):
        return self.name

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)
