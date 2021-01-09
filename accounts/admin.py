from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Profile, ResetPasswordCode


class UserAdmin(BaseUserAdmin):
    save_on_top = True
    list_display = (
        "id",
        "username",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
    )
    ordering = (
        "username",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
    )
    sortable_by = ("username",)
    search_fields = ("username", "email")
    list_filter = ("is_superuser", "is_staff", "date_joined", "is_active")
    date_hierarchy = "date_joined"

    list_per_page = 10


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        "id",
        "user",
        "full_name",
        "bio",
        "contact",
        "birth_date",
        "address",
        "last_updated",
    )
    ordering = (
        "user",
        "full_name",
        "bio",
        "contact",
        "birth_date",
        "address",
        "last_updated",
    )
    list_filter = (
        ("user__date_joined", admin.DateFieldListFilter),
        ("last_updated", admin.DateFieldListFilter),
    )
    date_hierarchy = "user__date_joined"
    search_fields = ("user__username", "contact", "address", "full_name")
    autocomplete_fields = ["user"]

    fieldsets = (
        (
            "Personal Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": ("full_name", "contact", "bio", "birth_date", "image"),
            },
        ),
        (
            "Location Information",
            {"classes": ("wide", "extrapretty"), "fields": ("address",)},
        ),
    )
    list_per_page = 10

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


class ResetPasswordCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code")
    list_per_page = 10
    date_hierarchy = "user__date_joined"
    list_filter = ("user__date_joined",)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
admin.site.register(ResetPasswordCode, ResetPasswordCodeAdmin)
