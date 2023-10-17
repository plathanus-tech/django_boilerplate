from django.utils.translation import gettext_lazy as _


class Language:
    PT_BR = "pt-br"
    EN_US = "en-us"

    choices = [
        (PT_BR, _("Brazilian Portuguese")),
        (EN_US, _("English")),
    ]


class TimeZoneName:
    AMERICA_SAO_PAULO = "America/Sao_Paulo"
    UTC = "UTC"

    choices = [
        (AMERICA_SAO_PAULO, _("São Paulo - Brazil (-03:00)")),
        (UTC, _("Universal Coordinated Time")),
    ]
