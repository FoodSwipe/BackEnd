from django.contrib.auth import get_user_model
from django.db import models

from item.models import MenuItem


class Order(models.Model):
    custom_location = models.CharField(max_length=512, blank=True, null=True)
    is_delivered = models.BooleanField(default=False, editable=False)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=8, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="OrderCreator")

    def __str__(self):
        return "Order #{} -- {}".format(self.pk, self.created_by)


class CartItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="BaseOrder",
    )
    item = models.ForeignKey(
        MenuItem,
        on_delete=models.DO_NOTHING,
        related_name="CartItem"
    )
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        editable=False,
        related_name="CartItemCreator"
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('order', "item")

    def __str__(self):
        return self.item.name
