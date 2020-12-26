from django.contrib.auth import get_user_model
from django.db import models

from cart.models import Order


class Transaction(models.Model):
    order = models.OneToOneField(
        Order,
        related_name="TransactionOrder",
        on_delete=models.CASCADE
    )
    grand_total = models.DecimalField(default=0, decimal_places=2, max_digits=8, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        editable=False,
        related_name="TransactionCreator",
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return "{} -- Transaction #{}".format(self.created_by, self.pk)
