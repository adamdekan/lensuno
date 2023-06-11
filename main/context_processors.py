from .forms import SearchForm
from django.conf import settings


def theme(request):
    if "is_dark_theme" in request.session:
        is_dark_theme = request.session.get("is_dark_theme")
        return {"is_dark_theme": is_dark_theme}
    return {"is_dark_theme": False}


def forms(request):
    return {
        "form_search": SearchForm(),
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    }


def header(request):
    return {"black_header": False}
