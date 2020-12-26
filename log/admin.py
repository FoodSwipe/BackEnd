from django.contrib import admin

from log.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = (
        "mode",
        "timestamp",
        "actor",
        "detail",
    )
    list_filter = ("timestamp", "mode")
    date_hierarchy = 'timestamp'
    search_fields = ("mode", "actor__username", "detail")
    list_per_page = 10


admin.site.register(Log, LogAdmin)
