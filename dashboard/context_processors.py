from django.db import OperationalError, ProgrammingError

from .models import SiteBranding


def site_branding(request):
    try:
        branding = SiteBranding.get_solo()
    except (OperationalError, ProgrammingError):
        branding = None

    return {"site_branding": branding}
