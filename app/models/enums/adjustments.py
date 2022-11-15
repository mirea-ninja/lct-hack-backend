from .base_enum import BaseEnum


class Floor(int, BaseEnum):
    MINUS_310 = -310
    PLUS_0 = 0
    PLUS_320 = 320
    MINUS_400 = -400
    PLUS_420 = 420
    MINUS_700 = -700
    PLUS_750 = 750


class AptArea(int, BaseEnum):
    MINUS_2200 = -2200
    MINUS_1700 = -1700
    MINUS_1200 = -1200
    MINUS_1100 = -1100
    MINUS_700 = -700
    MINUS_600 = -600
    PLUS_0 = 0
    PLUS_300 = 300
    PLUS_600 = 600
    PLUS_700 = 700
    PLUS_900 = 900
    PLUS_1300 = 1300
    PLUS_1400 = 1400
    PLUS_1600 = 1600
    PLUS_2100 = 2100
    PLUS_2400 = 2400
    PLUS_2800 = 2800
    PLUS_3100 = 3100


class KitchenArea(int, BaseEnum):
    MINUS_830 = -830
    MINUS_550 = -550
    MINUS_290 = -290
    PLUS_300 = 300
    PLUS_580 = 580
    PLUS_900 = 900


class HasBalcony(int, BaseEnum):
    MINUS_500 = -500
    PLUS_0 = 0
    PLUS_530 = 530


class DistanceToMetro(int, BaseEnum):
    MINUS_2200 = -2200
    MINUS_1900 = -1900
    MINUS_1700 = -1700
    MINUS_1500 = -1500
    MINUS_1300 = -1300
    MINUS_1100 = -1100
    MINUS_1000 = -1000
    MINUS_900 = -900
    MINUS_800 = -800
    MINUS_700 = -700
    MINUS_600 = -600
    MINUS_500 = -500
    MINUS_400 = -400
    PLUS_0 = 0
    PLUS_400 = 400
    PLUS_500 = 500
    PLUS_600 = 600
    PLUS_700 = 700
    PLUS_900 = 900
    PLUS_1000 = 1000
    PLUS_1100 = 1100
    PLUS_1200 = 1200
    PLUS_1500 = 1500
    PLUS_1700 = 1700
    PLUS_2000 = 2000
    PLUS_2400 = 2400
    PLUS_2900 = 2900


class Quality(int, BaseEnum):
    MINUS_20100 = -20100
    MINUS_13400 = -13400
    MINUS_6700 = -6700
    PLUS_0 = 0
    PLUS_6700 = 6700
    PLUS_13400 = 13400
    PLUS_20100 = 20100


class AdjustmentType(str, BaseEnum):
    APT_AREA = "apt_area"
    KITCHEN_AREA = "kitchen_area"
    TO_METRO = "to_metro"
    HAS_BALCONY = "has_balcony"
    FLOOR = "floor"
    REPAIR_TYPE = "repair_type"
