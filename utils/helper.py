import os

from django.utils import timezone

from backend.settings import (DELIVERY_CHARGE, DELIVERY_START_AM,
                              DELIVERY_START_PM, LOYALTY_10_PER_FROM,
                              LOYALTY_12_PER_FROM, LOYALTY_13_PER_FROM,
                              LOYALTY_15_PER_FROM)


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
