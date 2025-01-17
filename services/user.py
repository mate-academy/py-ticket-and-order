from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> User:
    data_user = {}
    if email:
        data_user["email"] = email
    if first_name:
        data_user["first_name"] = first_name
    if last_name:
        data_user["last_name"] = last_name

    return User.objects.create_user(
        username=username,
        password=password,
        **data_user
    )


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> None:
    user = get_user(user_id)

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
