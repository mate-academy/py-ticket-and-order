from typing import Optional
from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order
from services.movie_session import get_movie_session_by_id


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=get_movie_session_by_id(ticket["movie_session"]),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: Optional[str] = None) -> list[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
