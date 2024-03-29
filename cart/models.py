from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from item.models import MenuItem

PAYMENT_CHOICES = [("Cash", "Cash")]


class Order(models.Model):
    custom_location = models.CharField(max_length=512, null=True, blank=True)
    custom_contact = PhoneNumberField(null=True, blank=True)
    custom_email = models.EmailField(null=True)
    total_price = models.DecimalField(
        default=0, decimal_places=2, max_digits=8, editable=False
    )
    delivery_started = models.BooleanField(default=False)
    delivery_started_at = models.DateTimeField(null=True, blank=True, editable=False)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True, editable=False)
    delivery_charge = models.PositiveIntegerField(default=0)
    loyalty_discount = models.PositiveBigIntegerField(default=0, editable=False)
    grand_total = models.PositiveBigIntegerField(default=0, editable=False)
    done_from_customer = models.BooleanField(default=False)
    done_from_customer_at = models.DateTimeField(null=True)
    total_items = models.PositiveBigIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default="Cash"
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="OrderCreator",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="OrderUpdater",
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Order #{} -- {}".format(self.pk, self.created_by)

    class Meta:
        ordering = ["-updated_at"]


class CartItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    item = models.ForeignKey(
        MenuItem, on_delete=models.DO_NOTHING, related_name="CartItem"
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False,
        related_name="CartItemCreator",
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ("order", "item")

    def __str__(self):
        return self.item.name

    class Meta:
        ordering = ["-updated_at"]


class MonthlySalesReport(models.Model):
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.DO_NOTHING, related_name="menu_item_sales"
    )
    sale_count = models.PositiveBigIntegerField(null=True)
    date = models.CharField(max_length=7)


class OrderKOT(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_kot")
    cart_item = models.ForeignKey(
        CartItem, on_delete=models.DO_NOTHING, related_name="kot_cart_item"
    )
    quantity_diff = models.BigIntegerField(
        default=0, help_text="Quantity difference from previous batch of this KOT item"
    )
    batch = models.PositiveBigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: #{}, Batch: {}".format(self.order.id, self.batch)

    class Meta:
        unique_together = [["order", "cart_item", "batch"]]
        verbose_name = "Order KOT"
        verbose_name_plural = "Order KOTs"
        ordering = ["-timestamp"]
