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


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int, password: str = None, first_name: str = None,
                last_name: str = None,
                email: str = None, username: str = None) -> None:
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
