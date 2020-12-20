import os
import random

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from item_group.models import MenuItemGroup


def upload_menu_item_media_to(instance, filename):
    item_name = instance.name
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'menu_item/{item_name}/{filename}'


def upload_menu_type_badge_to(instance, filename):
    type_name = instance.name
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'item_badge/{type_name}/{filename}'


class ItemType(models.Model):
    name = models.CharField(max_length=64, unique=True)
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


class Item(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(
        max_length=512,
        null=True, blank=True,
        help_text="Add features, specialities or uniqueness about the item."
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="in Rupees")
    is_available = models.BooleanField(default=True, verbose_name="Is available on store?")
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

    menu_item_group = models.ForeignKey(
        MenuItemGroup,
        null=True,
        blank=True,
        related_name="menu_items",
        on_delete=models.SET_NULL
    )
    image = models.ImageField(
        upload_to=upload_menu_item_media_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )

    class Meta:
        abstract = True

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)


class MenuItem(Item):
    ingredients = ArrayField(models.CharField(max_length=64), size=20)
    scale = models.IntegerField(default=1,
                                help_text="Scale for price i.e. how much (quantity / weight(ml)) on this price?")
    weight = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="in grams for regular item and ml for bar item"
    )
    calorie = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="in kCal")
    is_veg = models.BooleanField(verbose_name="Is vegetarian item?", default=False)
    item_type = models.ManyToManyField(
        ItemType,
        help_text="You can select multiple item types.",
        blank=True,
        related_name="item_types"
    )

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.name
