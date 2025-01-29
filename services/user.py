from django.db.models import QuerySet

from db.models import User

def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,

):
    user = User.objects.create_user(username=username, password=password)

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()

    return user

def get_user(user_id: int):
    return User.objects.get(pk=user_id)


def update_user(user_id: int, username: str, password: str, email: str = None, first_name: str = None, last_name: str = None):
    user = User.objects.get(pk=user_id)

    if email:
        user.email = email
    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.set_password(password)

    user.save()
    return user
