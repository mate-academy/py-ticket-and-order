from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> User:
    user = super().create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user
    
    
def get_user(user_id: int) -> User:
    try:
        User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    
    
def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
):
    try:
        user = User.objects.get(id=user_id)
        user.username = username
        user.set_password(password)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    except User.DoesNotExist:
        pass
    