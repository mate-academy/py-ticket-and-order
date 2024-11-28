from django.contrib.auth import get_user_model

User = get_user_model

def create_user(username, password, **kwargs):
    return User.objects.create_user(username=username, password=password, **kwargs)

def get_user(user_id):
    return User.objects.filter(id=user_id).first()

def update_user(user_id, **kwargs):
    user = get_user(user_id)
    if user:
        if "password" in kwargs:
            user.set_password(kwargs.pop("password"))
        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
    return user
