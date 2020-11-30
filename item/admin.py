from django.contrib import admin

from item.models import ItemType, MenuItem, MenuItemImage, MenuItemType


class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "badge")
    list_per_page = 10


class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "menu_item_group",
        "price",
        "ingredients",
        "is_veg",
        "is_available",
        "discount",
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
        "discount",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by"
    )
    list_filter = (
        "is_veg",
        "is_available",
        "menu_item_group",
    )
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
            )
        }),
        ("Business Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "price",
                "discount",
                "is_available"
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


class MenuItemImageAdmin(admin.ModelAdmin):
    list_display = ("menu_item", "image")
    list_per_page = 10
    ordering = ("menu_item",)
    search_fields = ("menu_item__name",)
    date_hierarchy = "menu_item__created_at"

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


class MenuItemTypeAdmin(admin.ModelAdmin):
    list_display = ("menu_item", )
    list_per_page = 10
    ordering = ("menu_item",)
    search_fields = ("menu_item__name",)

    list_filter = ("item_type",)

    filter_horizontal = ("item_type",)
    date_hierarchy = "menu_item__created_at"


admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(MenuItemImage, MenuItemImageAdmin)
admin.site.register(MenuItemType, MenuItemTypeAdmin)
