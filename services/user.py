from db.models import User


def create_user(password: str, username: str,
                first_name: str = None,
                last_name: str = None, email: str = None) -> None:
    user = User.objects.create_user(username=username, password=password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    user.save()


def get_user(user_id: int) -> None | User:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def update_user(user_id: int, password: str = None, first_name: str = None,
                last_name: str = None,
                email: str = None, username: str = None) -> None:
    try:
        user = User.objects.get(id=user_id)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if password:
            user.set_password(password)
        if username:
            user.username = username
        user.save()
    except User.DoesNotExist:
        return None
