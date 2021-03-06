from datetime import timedelta
from typing import Any, Dict, Tuple
from refreshing_token.models import RefreshToken,AccessToken
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

# TODO: write tests
# TODO: docs

def is_token_expired(token: Any, lifetime: timedelta):
    min_age = timezone.now() - lifetime
    expired = token.created < min_age
    return expired

def generate_token_pair(user: AbstractUser) -> Dict[str,str]:
    """
    generates token pair for given user, user object must be of same type
    as settings.AUTH_USER_MODEL, returns a dict with access_token and 
    refresh_token.
    if a token pair is already generated it is replaced by the
    newly generated one.
    """
    AccessToken.objects.filter(user=user).delete()
    RefreshToken.objects.filter(user=user).delete()
    access_token = AccessToken.objects.create(user=user)
    refresh_token = RefreshToken.objects.create(user=user)
    return {"access_token":access_token.key,
        "refresh_token":refresh_token.key}

def discard_refresh_token(token: str, user: AbstractUser) -> bool:
    """
    discard given refresh token, user argument is needed
    because a user should not be able to delete someone else's
    refresh token, doesn't return an error, returns True, 
    if something really was deleted or else False.
    """
    count,_ = RefreshToken.objects.filter(key=token,user=user).delete()
    return count > 0

def discard_access_token(token: str, user: AbstractUser) -> bool:
    """
    discard given access token, user argument is needed
    because a user should not be able to delete someone else's
    access token. doesn't return an error, returns True, 
    if something really was deleted or else False.
    """
    count,_ = AccessToken.objects.filter(key=token,user=user).delete()
    return count > 0

def clean_refresh_tokens(user: AbstractUser) -> bool:
    """
    deletes refresh tokens of a given user,
    could be useful, generally i have seen in whereever JWT is used
    in the case of logout, only the refresh token is blacklisted/deleted,
    don't really know why that is.
    """
    count,_ = RefreshToken.objects.filter(user=user).delete()
    return count > 0

def clean_access_tokens(user: AbstractUser) -> bool:
    """
    function for deleting access tokens of given user
    """
    count,_ = AccessToken.objects.filter(user=user).delete()
    return count > 0

def clean_user_tokens(user: AbstractUser) -> Tuple[bool,bool]:
    """
    delete both access and refresh tokens in one go
    returns a tuple of two bools, first value is for 
    access token and the second one for refresh token.
    """
    count,_ = AccessToken.objects.filter(user=user).delete()
    count_a,_ = RefreshToken.objects.filter(user=user).delete()
    return (count > 0,count_a > 0)

def create_access_token(user: AbstractUser, key: str = None) -> Tuple[str,bool]:
    """
    function for creating access token individually with an optional param for key
    in case one want to use their own defined key as access token
    """
    count,_ = AccessToken.objects.filter(user=user).delete()
    token = AccessToken.objects.create(user=user,key=key)
    return token.key, count > 0

def create_refresh_token(user: AbstractUser, key: str = None) -> Tuple[str,bool]:
    """
    function for creating access token individually with an optional param for key
    in case one want to use their own defined key as refresh token
    """
    count,_ = RefreshToken.objects.filter(user=user).delete()
    token = RefreshToken.objects.create(user=user,key=key)
    return token.key, count > 0

def refresh_access_token(refresh_token: str, key: str = None) -> str:
    try:
        expiry = settings.REFRESH_TOKEN_LIFETIME
    except AttributeError:
        expiry = timedelta(days=1)
    
    try:
        token_obj = RefreshToken.objects.get(key=refresh_token)
    except RefreshToken.DoesNotExist:
        raise AuthenticationFailed("Invalid Refresh token")

    expired = is_token_expired(token_obj,expiry)
    if expired:
        clean_user_tokens(token_obj.user)
        raise AuthenticationFailed("Refresh Token has expired")

    access_token,_ = create_access_token(token_obj.user,key)

    return access_token

# have to take it for a spin
def get_or_create_token_pair(user: AbstractUser) -> Dict[str,str]:
    """
    utility function for returning same token pair if it already exists
    it could be useful in case you don't want a user to be logged out from
    one device if they log in from another, ideally every device should have its own
    token pair.
    If refresh token is expired or isn't found both refresh token and access token
    are generated entirely, but if only the access token is expired it is generated and current
    active refresh token is returned.
    """
    try:
        access_expiry = settings.ACCESS_TOKEN_LIFETIME
    except AttributeError:
        access_expiry = timedelta(minutes=60)

    try:
        refresh_expiry = settings.REFRESH_TOKEN_LIFETIME
    except AttributeError:
        refresh_expiry = timedelta(days=1)

    refresh_token,_ = RefreshToken.objects.get_or_create(user=user)
    refresh_expired = is_token_expired(refresh_token,refresh_expiry)
    if refresh_expired:
        clean_user_tokens(user=user)
        return generate_token_pair(user=user)
    
    access_token,_ = AccessToken.objects.get_or_create(user=user)
    access_expired = is_token_expired(access_token,access_expiry)
    if access_expired:
        clean_access_tokens(user=user)
        new_access_token,_ = create_access_token(user=user)
        return {"access_token":new_access_token,
            "refresh_token":refresh_token.key
        }
    return {
        "access_token":access_token.key,
        "refresh_token":refresh_token.key
    }

    


    




