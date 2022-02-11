from typing import Tuple
from rest_framework.authtoken.models import Token
from refreshing_token.models import RefreshToken
from django.contrib.auth.models import AbstractUser


def generate_token_pair(user: AbstractUser):
    """
    generates token pair for given user, user object must be of same type
    as settings.AUTH_USER_MODEL, returns a dict with access_token and 
    refresh_token.
    """
    Token.objects.filter(user=user).delete()
    RefreshToken.objects.filter(user=user).delete()
    access_token = Token.objects.create(user=user)
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
    count,_ = Token.objects.filter(key=token,user=user).delete()
    return count > 0

def clean_refresh_tokens(user: AbstractUser) -> bool:
    """
    deletes refresh tokens of a given user,
    could be useful, generally i have seen in whereever JWT is used
    in the case of logout, only the refresh token is blacklisted/deleted,
    don't really know why that is.
    """
    count,_ = RefreshToken.objects.filter(user).delete()
    return count > 0

def clean_access_tokens(user: AbstractUser) -> bool:
    """
    function for deleting access tokens of given user
    """
    count,_ = Token.objects.filter(user).delete()
    return count > 0

def clean_user_tokens(user: AbstractUser) -> Tuple[bool,bool]:
    """
    delete both access and refresh tokens in one go
    returns a tuple of two bools, first value is for 
    access token and the second one for refresh token.
    """
    count,_ = Token.objects.filter(user).delete()
    count_a,_ = RefreshToken.objects.filter(user).delete()
    return (count > 0,count_a > 0)