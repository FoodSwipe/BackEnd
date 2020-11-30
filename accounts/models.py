import os
import random
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


def upload_posts_media_to(instance, filename):
    username = instance.profile.user.username
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'profile/{username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False
    )
    bio = models.TextField(null=True, blank=True, max_length=1024)
    contacts = ArrayField(
        models.PositiveBigIntegerField(unique=True),
        size=3,
        null=True,
        blank=True
    )
    birth_date = models.DateField(null=True, blank=True)
    current_city = models.CharField(max_length=512, blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username + ' Profile'

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


class ProfileImage(models.Model):
    image = models.ImageField(
        upload_to=upload_posts_media_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="FollowerProfileImage"
    )

    class Meta:
        verbose_name = "Customer Profile Image"
        verbose_name_plural = "Customer Profile Images"

    def __str__(self):
        return self.profile.user.username

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        verbose_name_plural = "Reset Password Codes"

    def __str__(self):
        return "{} - {}".format(self.user.username, self.code)
