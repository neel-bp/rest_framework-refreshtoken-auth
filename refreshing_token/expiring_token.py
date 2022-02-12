from datetime import timedelta
from rest_framework.authentication import TokenAuthentication
from refreshing_token.models import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from refreshing_token.util import is_token_expired
from django.conf import settings




class ExpiringTokenAuthentication(TokenAuthentication):

    model = AccessToken

    """Same as in DRF, but also handle Token expiration.
    
    An expired Token will be removed and a new Token with a different
    key is created that the User can obtain by logging in with his
    credentials.
    
    Raise AuthenticationFailed as needed, which translates
    to a 401 status code automatically.
    """
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted")

        try:
            lifetime = settings.ACCESS_TOKEN_LIFETIME
        except:
            lifetime = timedelta(minutes=60)

        expired = is_token_expired(token,lifetime)
        if expired:
            token.delete()
            # Token.objects.create(user=token.user)
            raise AuthenticationFailed("Token has expired")

        return (token.user, token)