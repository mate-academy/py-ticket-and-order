from datetime import datetime
from typing import Optional, Union

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(
    username: Optional[str] = None
) -> Union[QuerySet, User]:
    if username:
        return User.objects.get(username=username).order_set.all()
    return Order.objects.all()
