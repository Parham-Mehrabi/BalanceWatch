from django.conf import settings


def ui_theme(request):
    theme = request.COOKIES.get("theme", "dark")
    if theme not in settings.UI_THEMES:
            theme = "dark"
    
    context = {"theme": theme,
               "allowed_themes": settings.UI_THEMES}
    return context
