# core/templatetags/i18n_attrs.py
from django import template

register = template.Library()

@register.filter
def tattr(obj, base_field_with_lang):
    """
    Альтернатива: {{ product|tattr:"name:en" }}
    """
    try:
        base, lang = base_field_with_lang.split(":")
    except ValueError:
        return getattr(obj, base_field_with_lang, "")
    return _pick(obj, base, lang)

    return pick(obj, base_field, lang_code)
from decimal import Decimal  # не обязателен, но пусть будет
from django import template

register = template.Library()

def _pick(obj, base_field: str, lang: str) -> str:
    """
    Возвращает локализованное поле:
    <base>_<lang> → <base>_ru → <base>
    """
    # 1) base_lang
    f = f"{base_field}_{lang}"
    val = getattr(obj, f, "") or ""
    if val:
        return val
    # 2) fallback ru
    if lang != "ru":
        val = getattr(obj, f"{base_field}_ru", "") or ""
        if val:
            return val
    # 3) base
    return getattr(obj, base_field, "") or ""

@register.simple_tag(takes_context=True)
def t(context, obj, base_field: str):
    """
    Использование: {% t product "name" %} или {% t category "name" %}
    Берёт язык из LANGUAGE_CODE в контексте.
    """
    lang = context.get("LANGUAGE_CODE", "ru")
    return _pick(obj, base_field, lang)
