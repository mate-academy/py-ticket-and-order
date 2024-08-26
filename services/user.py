from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name or "",
            last_name=last_name or ""
        )
        return user
    except Exception as e:
        raise ValidationError(
            f"An error occurred while creating the user: {str(e)}"
        )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = User.objects.get(pk=user_id)

    if username:
        user.username = username
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.set_password(password)

    user.save()
    return user
