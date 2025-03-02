from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


def create_user(
    username: str,
    password: str,
    email: str = None,
    last_name: str = None,
    first_name: str = None,
) -> AUTH_USER_MODEL:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    if email:
        user.email = email

    if last_name:
        user.last_name = last_name

    if first_name:
        user.first_name = first_name

    user.save()

    return user


def get_user(user_id: int) -> AUTH_USER_MODEL:
    return get_object_or_404(get_user_model(), pk=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> AUTH_USER_MODEL:
    user = get_object_or_404(get_user_model(), pk=user_id)

    if username:
        user.username = username

    if password:
        user.set_password(password)

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    user.save()

    return user
