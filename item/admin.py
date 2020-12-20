from django.contrib import admin

from item.models import ItemType, MenuItem


class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "badge")
    list_per_page = 10


class MenuItemAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        "name",
        "menu_item_group",
        "price",
        "ingredients",
        "is_veg",
        "is_available",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by"
    )
    ordering = (
        "name",
        "menu_item_group",
        "price",
        "is_veg",
        "is_available",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by"
    )
    sortable_by = ("name",)
    list_filter = (
        "is_veg",
        "is_available",
        "menu_item_group",
        "created_at"
    )
    filter_horizontal = ("item_type",)
    search_fields = ("name", "menu_item_group__name", "ingredients")
    date_hierarchy = "created_at"
    autocomplete_fields = ("menu_item_group",)
    fieldsets = (
        ("Item Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name",
                "description",
                "ingredients",
                "menu_item_group",
                "weight",
                "calorie",
                "is_veg",
                "item_type"
            )
        }),
        ("Business Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "price",
                "is_available",
                "image"
            )
        })
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


admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
