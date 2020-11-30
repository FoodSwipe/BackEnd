import os
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


def upload_menu_item_group_media_to(instance, filename):
    item_name = instance.menu_item_group.name
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'menu_item_group/{item_name}/{filename}'


class MenuItemGroup(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=512)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="in Rupees")
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="in %")

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

    class Meta:
        verbose_name = "Menu Item Group"
        verbose_name_plural = "Menu Item Groups"

    def __str__(self):
        return self.name


class MenuItemGroupImage(models.Model):
    menu_item_group = models.ForeignKey(
        MenuItemGroup,
        on_delete=models.CASCADE,
        related_name="RelMenuItemForImage"
    )
    image = models.ImageField(
        upload_to=upload_menu_item_group_media_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )

    class Meta:
        verbose_name = "Menu Item Group Image"
        verbose_name_plural = "Menu Item Group Images"

    def __str__(self):
        return self.menu_item_group.name

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)
