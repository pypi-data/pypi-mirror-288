from . import app_settings as registration_app_settings
from .. import allauth_enabled

if allauth_enabled:
    from allauth.account.adapter import DefaultAccountAdapter

    class NinjaAccountAdapter(DefaultAccountAdapter):
        def get_email_confirmation_url(self, request, emailconfirmation):
            return f"{registration_app_settings.EMAIL_CONFIRMATION_URL}?key={emailconfirmation.key}"
