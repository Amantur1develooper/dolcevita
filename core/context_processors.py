# core/context_processors.py
def language_codes(request):
    lang = getattr(request, "LANGUAGE_CODE", "ru")
    return {"LANGUAGE_CODE": lang}
