from django.contrib import admin

from item_group.models import MenuItemGroup, MenuItemGroupImage


class MenuItemGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price",
        "discount",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )
    ordering = (
        "name",
        "description",
        "price",
        "discount",
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
            )
        }),
        ("Business Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "price",
                "discount",
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


class MenuItemGroupImageAdmin(admin.ModelAdmin):
    list_display = ("menu_item_group", "image")
    list_per_page = 10
    ordering = ("menu_item_group",)
    search_fields = ("menu_item_group__name",)
    date_hierarchy = "menu_item_group__created_at"

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


admin.site.register(MenuItemGroup, MenuItemGroupAdmin)
admin.site.register(MenuItemGroupImage, MenuItemGroupImageAdmin)
