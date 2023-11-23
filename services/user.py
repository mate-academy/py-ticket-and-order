from typing import Any, Optional

from django.contrib.auth import get_user_model


def create_user(
    username: str,
    password: Any,
    email: Optional[str] = None,
    first_name: str = "",
    last_name: str = "",
) -> get_user_model():
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user


def get_user(user_id: int) -> get_user_model():
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[Any] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> get_user_model():
    user = get_user_model()
    user = user.objects.get(id=user_id)

    if user:
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
