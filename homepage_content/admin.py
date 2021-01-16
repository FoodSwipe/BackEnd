from django.contrib import admin

from homepage_content.models import HomePageContent


class HomePageContentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "heading",
        "subtitle",
        "image",
        "button_text",
        "button_icon",
        "button_to",
        "created_at",
    )
    ordering = (
        "heading",
        "subtitle",
        "button_text",
        "button_icon",
        "button_to",
        "created_at",
    )
    sortable_by = (
        "heading",
        "subtitle",
        "button_text",
        "button_icon",
        "button_to",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("heading", "button_text")
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Home Page Content Item Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": (
                    "heading",
                    "subtitle",
                    "button_text",
                    "button_icon",
                    "button_to",
                ),
            },
        ),
    )

    list_per_page = 10

    def save_model(self, request, obj, form, change):
        print(obj.image)
        print(form.image)
        if "image" in form.changed_data:
            obj.image.delete()

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


admin.site.register(HomePageContent, HomePageContentAdmin)
