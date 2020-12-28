import os
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from item.models import MenuItem


def upload_review_image_to(instance, filename):
    reviewer_contact = str(instance.reviewer_contact)
    reviewed_item = instance.menu_item.name
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'review/{reviewer_contact[4:]}/{reviewed_item.replace(" ", "_")}/{filename}'


class Review(models.Model):
    review = models.TextField(max_length=1024)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, related_name="reviews", null=True)
    reviewer = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="reviews",
        null=True,
        editable=False
    )
    reviewer_contact = PhoneNumberField()
    image = models.ImageField(
        upload_to=upload_review_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
        null=True,
        blank=True
    )
    reviewed_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.reviewer_contact)

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)
