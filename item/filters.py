import django_filters

from item.models import MenuItem


class MenuItemFilter(django_filters.FilterSet):
    class Meta:
        model = MenuItem
        fields = {"name": ["contains"], "ingredients": ["contains"]}
