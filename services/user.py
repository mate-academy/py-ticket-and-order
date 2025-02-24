from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: str = "",
    first_name: str = "",
    last_name: str = ""
) -> User:
    user = User.objects.create(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = "",
    password: str = "",
    email: str = "",
    first_name: str = "",
    last_name: str = ""
) -> None:
    user = User.objects.get(id=user_id)
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
