from django.contrib import admin

from cart.models import CartItem, Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_by",
        "done_from_customer",
        "custom_location",
        "custom_contact",
        "custom_email",
        "total_price",
        "created_at",
        "updated_at",
    )
    ordering = (
        "created_by",
        "done_from_customer",
        "custom_location",
        "custom_contact",
        "custom_email",
        "total_price",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    search_fields = ("created_by__username", "custom_location", "custom_contact", "custom_email",)
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "item",
        "quantity",
        "created_at",
        "created_by",
        "updated_at"
    )
    ordering = (
        "order",
        "item",
        "quantity",
        "created_at",
        "created_by",
        "updated_at"
    )
    list_filter = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    search_fields = ("item__name", "created_by__username")
    autocomplete_fields = ("item",)
    list_per_page = 10
    save_as_continue = True
    fieldsets = (
        ("Cart Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "order",
                "item",
                "quantity",
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.order.total_price += obj.item.price * obj.quantity
            obj.order.save()
            obj.created_by = request.user
        if change:
            this_item = CartItem.objects.get(pk=obj.pk)
            if this_item.quantity != obj.quantity:
                # remove previous total
                obj.order.total_price -= obj.item.price * this_item.quantity
                # add updated total
                obj.order.total_price += obj.item.price * obj.quantity
                obj.order.save()
        super().save_model(request, obj, form, change)


admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem, CartAdmin)
