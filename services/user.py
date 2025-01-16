from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        email: str = None
) -> User:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    if first_name:
        new_user.first_name = first_name

    if last_name:
        new_user.last_name = last_name

    if email:
        new_user.email = email

    new_user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None
) -> User:
    update_user_info = get_user(user_id=user_id)

    if username:
        update_user_info.username = username

    if password:
        update_user_info.set_password(password)

    if email:
        update_user_info.email = email

    if first_name:
        update_user_info.first_name = first_name

    if last_name:
        update_user_info.last_name = last_name

    update_user_info.save()
