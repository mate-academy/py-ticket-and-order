from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    # Надійний парсинг дати
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError(f"Invalid date format: {date}. Expected format: YYYY-MM-DD HH:MM")

    if date is None:
        date = timezone.now()

    with transaction.atomic():
        # Обробка помилки, якщо користувача не існує
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError(f"User with username '{username}' does not exist.")

        order = Order.objects.create(
            created_at=date,
            user=user)

        for ticket in tickets:
            # Обробка помилки, якщо сеанс не існує
            try:
                movie_session = MovieSession.objects.get(id=ticket["movie_session"])
            except MovieSession.DoesNotExist:
                raise ValueError(f"Movie session with id {ticket['movie_session']} does not exist.")

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except User.DoesNotExist:
            raise ValueError(f"User with username '{username}' does not exist.")
    return Order.objects.all()
