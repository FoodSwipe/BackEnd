from django.contrib import admin

from transaction.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "grand_total",
        "created_at",
        "created_by",
    )
    ordering = (
        "order",
        "grand_total",
        "created_at",
        "created_by",
    )
    list_filter = ("created_at",)
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
            obj.grand_total = obj.order.grand_total
        super().save_model(request, obj, form, change)


admin.site.register(Transaction, TransactionAdmin)
