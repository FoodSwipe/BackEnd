import os
import random

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


def upload_menu_type_badge_to(instance, filename):
    type_name = instance.name
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'item_badge/{type_name}/{filename}'


class ItemType(models.Model):
    name = models.CharField(max_length=64)
    badge = models.ImageField(
        upload_to=upload_menu_type_badge_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
        help_text="Add badge image for this type of item."
    )

    class Meta:
        verbose_name = "Item Type"
        verbose_name_plural = "Item Types"

    def __str__(self):
        return self.name

    def clean(self):
        if self.badge.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.badge.delete()
        super().delete(using, keep_parents)


class MenuItem(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(
        max_length=512,
        help_text="Add features, specialities or uniqueness about the item."
    )
    ingredients = ArrayField(models.CharField(max_length=64), size=20)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="in grams")
    calorie = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="in kCal")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="in Rupees")
    is_veg = models.BooleanField(verbose_name="Is vegetarian item?")
    is_available = models.BooleanField(default=True, verbose_name="Is available on store?")
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="in %")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        editable=False,
        related_name="MenuItemCreator",
        on_delete=models.SET_NULL,
        null=True
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(
        get_user_model(),
        editable=False,
        related_name="MenuItemModifier",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.name


def upload_menu_item_media_to(instance, filename):
    item_name = instance.menu_item.name
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'menu_item/{item_name}/{filename}'


class MenuItemType(models.Model):
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="RelMenuItemForType"
    )
    item_type = models.ManyToManyField(ItemType, help_text="You can select multiple item types.")

    def __str__(self):
        return self.menu_item.name

    class Meta:
        verbose_name = "Menu Item Type"
        verbose_name_plural = "Menu Item Types"


class MenuItemImage(models.Model):
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="RelMenuItemForImage"
    )
    image = models.ImageField(
        upload_to=upload_menu_item_media_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )

    class Meta:
        verbose_name = "Menu Item Image"
        verbose_name_plural = "Menu Item Images"

    def __str__(self):
        return self.menu_item.name

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)
