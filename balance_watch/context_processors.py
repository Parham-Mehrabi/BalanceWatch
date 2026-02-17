from django.conf import settings


def ui_theme(request):
    theme = request.COOKIES.get("theme", "night")
    if theme not in settings.UI_THEMES:
            theme = "night"
    
    context = {"theme": theme,
               "allowed_themes": settings.UI_THEMES}
    return context
