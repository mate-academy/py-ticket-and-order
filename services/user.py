from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ):
    user = User.objects.create_user(username=username)
    user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id):
    return User.objects.get(id=user_id)


def update_user(user_id,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None):
    user = get_user(user_id=user_id)
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
