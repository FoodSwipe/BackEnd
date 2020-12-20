from django.contrib import admin

from item_group.models import MenuItemGroup


class MenuItemGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )
    ordering = (
        "name",
        "description",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )
    search_fields = ("name",)
    date_hierarchy = "created_at"
    fieldsets = (
        ("Item Group Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name",
                "description",
                "image"
            )
        }),
    )
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


admin.site.register(MenuItemGroup, MenuItemGroupAdmin)
