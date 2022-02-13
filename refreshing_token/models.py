import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class RefreshToken(Token):
    key = models.CharField(_("Key"), max_length=256, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='refresh_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )

    class Meta:
        verbose_name = _("RefreshToken")
        verbose_name_plural = _("RefreshTokens")

class RefreshTokenProxy(RefreshToken):
    """
    Proxy mapping pk to user pk for use in admin.
    """
    @property
    def pk(self):
        return self.user_id

    class Meta:
        proxy = 'refreshing_token' in settings.INSTALLED_APPS
        verbose_name = "refresh_token"

class AccessToken(Token):
    key = models.CharField(_("Key"), max_length=256, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='access_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )

    class Meta:
        verbose_name = _("AccessToken")
        verbose_name_plural = _("AccessTokens")

class AccessTokenProxy(AccessToken):

    class Meta:
        proxy = 'refreshing_token' in settings.INSTALLED_APPS
        verbose_name = "access_token"
