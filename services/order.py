from django.utils import timezone
from db.models import User, Ticket, Order, MovieSession
from typing import Optional
from django.db import transaction


def create_order(*, username, tickets, date=None):

    with transaction.atomic():
        user = User.objects.get(username=username)

        # Якщо дата не передана, використовуємо поточний час
        if not date:
            date = timezone.now()

        # Створення замовлення
        order = Order.objects.create(user=user, created_at=date)

        # Створення квитків для цього замовлення
        for ticket in tickets:
            movie_session = MovieSession.objects.get(id=ticket['movie_session'])
            Ticket.objects.create(
                order=order,
                row=ticket['row'],
                seat=ticket['seat'],
                movie_session=movie_session,

            )

        return order



def get_orders(username: Optional[str] = None) -> list[Order]:
    if username:
        if not User.objects.filter(username=username).exists():
            raise ValueError(f"User with username '{username}' does not exist.")
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
