from django.contrib.auth.backends import BaseBackend
from .models import ConfirmationCode


class ConfirmationCodeBackend(BaseBackend):
    def authenticate(self, request, username=None, confirmation_code=None):
        if ConfirmationCode.objects.filter(
            user__username=username,
            confirmation_code=confirmation_code
        ).exists():
            return ConfirmationCode.objects.filter(
                user__username=username,
                confirmation_code=confirmation_code).last().user
        return None
