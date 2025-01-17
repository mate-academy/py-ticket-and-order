from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    if email:
        new_user.email = email
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name
    new_user.save()
    return new_user


def get_user(user_id: int) -> User:
    try:
        user_to_get = get_user_model().objects.get(pk=user_id)
    except get_user_model().DoesNotExist:
        print(f"User with id: {user_id} not found")
    return user_to_get


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:
    try:
        user_to_update = get_user_model().objects.get(pk=user_id)
    except get_user_model().DoesNotExist:
        print(f"User with id: {user_id} not found")

    if username:
        user_to_update.username = username
    if password:
        user_to_update.set_password(password)
    if email:
        user_to_update.email = email
    if first_name:
        user_to_update.first_name = first_name
    if last_name:
        user_to_update.last_name = last_name
    user_to_update.save()
