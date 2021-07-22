import os

from django.utils import timezone

from backend.settings import (DELIVERY_CHARGE, DELIVERY_START_AM,
                              DELIVERY_START_PM, LOYALTY_10_PER_FROM,
                              LOYALTY_12_PER_FROM, LOYALTY_13_PER_FROM,
                              LOYALTY_15_PER_FROM)


def generate_url_for_media_resources_in_object(serializer, object_name=None):
    front = "http" if os.getenv("IS_SECURE") else "https"
    if object_name is None:
        object_name = {}
    for target, field_name in object_name.items():
        if isinstance(serializer.data[target], list):
            for pivot_target in serializer.data[target]:
                pivot_target[field_name] = "{}://{}{}".format(
                    front, os.getenv("BASE_URL"), pivot_target[field_name]
                )
        else:
            t = serializer.data[target]
            t[field_name] = "{}://{}{}".format(
                front, os.getenv("BASE_URL"), t[field_name]
            )
    return serializer


def generate_url_for_media_resources(serializer, param="image"):
    for target in serializer.data:
        front = "http" if os.getenv("IS_SECURE") else "https"
        if target[param]:
            target[param] = "{}://{}{}".format(
                front, os.getenv("BASE_URL"), target[param]
            )
    return serializer


def generate_url_for_media_resource(serializer, param="image"):
    front = "http" if os.getenv("IS_SECURE") else "https"
    serializer[param] = "{}://{}{}".format(
        front, os.getenv("BASE_URL"), serializer[param]
    )
    return serializer


def get_delivery_charge():
    current_hour = int(timezone.datetime.now().strftime("%H"))
    if current_hour >= DELIVERY_START_PM or current_hour <= DELIVERY_START_AM:
        return DELIVERY_CHARGE
    else:
        return 0


def get_loyalty_discount(total_price):
    if LOYALTY_10_PER_FROM <= total_price < LOYALTY_12_PER_FROM:
        return 10
    elif LOYALTY_12_PER_FROM <= total_price < LOYALTY_13_PER_FROM:
        return 12
    elif LOYALTY_13_PER_FROM <= total_price < LOYALTY_15_PER_FROM:
        return 13
    elif total_price >= LOYALTY_15_PER_FROM:
        return 15
    else:
        return 0
