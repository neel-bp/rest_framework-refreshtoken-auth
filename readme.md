---
this package adds some extra features to 
djangorestframework's Token Authentication like refresh
token, lifetime for refresh token and authorization token.

## requirements
* django
* djagnorestframework

## installation
`pip install git+https://github.com/neel-bp/rest_framework-refreshtoken-auth.git`

## instructions

add `refreshing_token` to `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'refreshing_token'
    ...
]
```

add `refreshing_token.expiring_token.ExpiringTokenAuthentication` to the 
list of authentication classes

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'refreshing_token.expiring_token.ExpiringTokenAuthentication',
    )
    ...
}
```

finally run `python manage.py migrate` in your django project
