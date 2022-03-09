from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

register = template.Library()


@register.filter
@stringfilter
def switch_i18n_prefix(path, language):
    return switch_lang_code(path, language)


@register.filter
def switch_i18n(request, language):
    return switch_lang_code(request.get_full_path(), language)


def switch_lang_code(path, language):
    lang_codes = [c for (c, _) in settings.LANGUAGES]

    paths = path.split("/")
    if paths[1] in lang_codes:
        paths[1] = language
    else:
        paths[0] = "/" + language

    return "/".join(paths)
