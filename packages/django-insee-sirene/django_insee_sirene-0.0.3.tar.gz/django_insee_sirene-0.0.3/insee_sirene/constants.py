# Django
from django.utils.translation import gettext as _

TRANCHE_EFFECTIFS_CHOICES = {
    "00": _("0 salarié"),
    "01": _("1 ou 2 salariés"),
    "02": _("3 à 5 salariés"),
    "03": _("6 à 9 salariés"),
    "11": _("10 à 19 salariés"),
    "12": _("20 à 49 salariés"),
    "21": _("50 à 99 salariés"),
    "22": _("100 à 199 salariés"),
    "31": _("200 à 249 salariés"),
    "32": _("250 à 499 salariés"),
    "41": _("500 à 999 salariés"),
    "42": _("1 000 à 1 999 salariés"),
    "51": _("2 000 à 4 999 salariés"),
    "52": _("5 000 à 9 999 salariés"),
    "53": _("10 000 salariés et plus"),
    "NN": _("Non employeuse"),
}

TRANCHE_EFFECTIFS_ETABLISSEMENT_TO_EFFECTIFS_MAPPING = {
    "00": {"min": 0, "max": 0},
    "01": {"min": 1, "max": 2},
    "02": {"min": 3, "max": 5},
    "03": {"min": 6, "max": 9},
    "11": {"min": 10, "max": 19},
    "12": {"min": 20, "max": 49},
    "21": {"min": 50, "max": 99},
    "22": {"min": 100, "max": 199},
    "31": {"min": 200, "max": 249},
    "32": {"min": 250, "max": 499},
    "41": {"min": 500, "max": 999},
    "42": {"min": 1000, "max": 1999},
    "51": {"min": 2000, "max": 4999},
    "52": {"min": 5000, "max": 9999},
    "53": {"min": 10000, "max": None},
    "NN": {"min": None, "max": None},
}
