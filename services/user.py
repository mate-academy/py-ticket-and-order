from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    first_name = first_name or ""
    last_name = last_name or ""
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    try:
        user = User.objects.get(pk=user_id)
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
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"User with id {user_id} does not exist.")
