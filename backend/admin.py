from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    site_header = "Food Swipe Administration"
    site_title = "Food Swipe Administration"
    index_title = "Administration Dashboard"
    enable_nav_sidebar = False
    _empty_value_display = "null"
