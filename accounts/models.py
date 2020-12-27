import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


def upload_posts_media_to(instance, filename):
    username = instance.user.username
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'profile/{username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False,
        related_name="profile"
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(null=True, blank=True, max_length=1024)
    contact = PhoneNumberField(unique=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    image = models.ImageField(
        upload_to=upload_posts_media_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )

    def __str__(self):
        return self.user.username + ' Profile'

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        verbose_name_plural = "Reset Password Codes"

    def __str__(self):
        return "{} - {}".format(self.user.username, self.code)


class RegistrationMonthlyCount(models.Model):
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=12)
    count = models.PositiveBigIntegerField(null=True)

    class Meta:
        unique_together = [["year", "month"]]
