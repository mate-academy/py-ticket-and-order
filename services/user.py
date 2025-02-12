from db.models import User, MovieSession


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = "",
) -> None:
    User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
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


def get_taken_seats(movie_session_id: int) -> list[dict]:
    our_list = []
    for ticket in MovieSession.objects.get(pk=movie_session_id).ticket_set:
        our_list.append(
            {
                "row": ticket.row,
                "seat": ticket.seat,
            }
        )
    return our_list
