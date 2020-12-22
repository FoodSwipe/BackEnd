from django.contrib import admin

from transaction.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "grand_total",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )
    ordering = (
        "order",
        "grand_total",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("created_by__username", )
    date_hierarchy = "created_at"
    autocomplete_fields = ("order",)
    fieldsets = (
        ("Transaction Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "order",
            )
        }),
    )
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.grand_total = obj.order.total_price
        else:
            obj.updated_by = request.user
            obj.grand_total = obj.order.total_price
        super().save_model(request, obj, form, change)


admin.site.register(Transaction, TransactionAdmin)
