import os
import random

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, HOMEPAGE_CONTENT_IMAGE_MAX_SIZE


def upload_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"homepage_content/{filename}"


class HomePageContent(models.Model):
    heading = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=512)
    image = models.ImageField(
        upload_to=upload_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    button_text = models.CharField(max_length=64)
    button_icon = models.CharField(max_length=64)
    button_to = models.CharField(max_length=64)
    created_at = models.DateField(auto_now=True, editable=False)

    def __str__(self):
        return self.button_text

    def clean(self):
        if self.image.size / 1000 > HOMEPAGE_CONTENT_IMAGE_MAX_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")
