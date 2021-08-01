from django.contrib.auth import get_user_model
from django.db import models

LOG_MODES_CHOICES = [
    ("create", "Create"),
    ("update", "Update"),
    ("delete", "Delete"),
    ("done", "Done From Customer"),
    ("start", "Delivery Started"),
    ("complete", "Delivery Completed"),
]


class Log(models.Model):
    mode = models.CharField(max_length=8, choices=LOG_MODES_CHOICES, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    actor = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        editable=False,
        on_delete=models.CASCADE,
    )
    detail = models.CharField(max_length=512, editable=False)

    def __str__(self):
        return "({}) {}".format(self.mode, self.actor.username)

    class Meta:
        ordering = ['-timestamp']
