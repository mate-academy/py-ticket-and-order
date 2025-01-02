from db.models import User
from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None:
    user = get_user_model().objects.get(id=user_id)
    if password := kwargs.get("password"):
        kwargs["password"] = user.set_password(password)
    user.update(**kwargs)
