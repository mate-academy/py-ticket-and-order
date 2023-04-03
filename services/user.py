import init_django_orm  # noqa: F401

from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:

    created_user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    updated_user = get_user_model().objects.get(username=username)
    if email:
        updated_user.email = email

    if first_name:
        updated_user.first_name = first_name

    if last_name:
        updated_user.last_name = last_name

    updated_user.save()

    return created_user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    updated_user = get_user_model().objects.get(id=user_id)

    if username:
        updated_user.username = username

    if password:
        updated_user.set_password(password)

    if email:
        updated_user.email = email

    if first_name:
        # updated_user.first_names = first_name
        updated_user.first_name = first_name
    if last_name:
        updated_user.last_name = last_name

    updated_user.save()
