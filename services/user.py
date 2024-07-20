from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    new_user = User.objects.create_user(username=username)
    new_user.set_password(password)
    if email:
        new_user.email = email
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name

    new_user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    updating_user = User.objects.get(
        id=user_id
    )
    if username:
        updating_user.username = username
    if password:
        updating_user.set_password(password)
    if email:
        updating_user.email = email
    if first_name:
        updating_user.first_name = first_name
    if last_name:
        updating_user.last_name = last_name

    updating_user.save()
