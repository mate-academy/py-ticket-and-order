import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[datetime] = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date is not None:
            order.created_at = date
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )


def get_orders(
        username: Optional[str] = None
) -> QuerySet:
    return (
        Order.objects.filter(user__username=username)
        if username is not None else Order.objects.all()
    )
