from setuptools import setup

setup(
    name="refreshing_token",
    version="0.1",
    description="extentsion to django_restframework Token Authentication with expiry, and separate refresh token",
    author="neelu",
    author_email="neelu0@protonmail.com",
    packages=["refreshing_token"],
    install_requires = ["django","djangorestframework"],
    url='https://github.com/neel-bp/rest_framework-refreshtoken-auth'
)