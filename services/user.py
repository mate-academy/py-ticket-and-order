from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                email:str = None,
                first_name: str = None,
                last_name: str = None) -> User:

    user = User.objects.create_user(username, password)

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> User:
    #return User.objects.all()
    pass
def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:

