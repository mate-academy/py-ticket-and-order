from datetime import datetime
from typing import Any

from django.db import transaction

from db.models import Ticket, User, Order, MovieSession


def create_order(tickets: list, username: str,
                 date: datetime = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(
            user=user, created_at=date if date else datetime.now()
        )

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )
        return order


def get_orders(username: str = None) -> Any:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
