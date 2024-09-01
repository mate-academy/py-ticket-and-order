from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> None:
    if any(
        [
            username is not None,
            password is not None,
            email is not None,
            first_name is not None,
            last_name is not None
        ]
    ):
        user_to_update = get_user_model().objects.get(pk=user_id)

        if password:
            user_to_update.set_password(password)
        if username:
            user_to_update.username = username
        if email:
            user_to_update.email = email
        if first_name:
            user_to_update.first_name = first_name
        if last_name:
            user_to_update.last_name = last_name

        user_to_update.save()
