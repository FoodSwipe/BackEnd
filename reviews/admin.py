from django.contrib import admin

from reviews.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "review",
        "menu_item",
        "reviewer",
        "reviewer_contact",
        "reviewed_at",
        "updated_at",
    ]
    ordering = [
        "review",
        "menu_item",
        "reviewer",
        "reviewer_contact",
        "reviewed_at",
        "updated_at",
    ]

    list_filter = (
        "reviewed_at",
        "updated_at",
    )
    date_hierarchy = "reviewed_at"
    search_fields = (
        "reviewer__username",
        "reviewer_contact",
        "review",
        "menu_item__name",
    )
    autocomplete_fields = ["menu_item", "reviewer"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    list_per_page = 10


admin.site.register(Review, ReviewAdmin)
