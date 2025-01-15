from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession, User


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: Optional[datetime] = None,
) -> Order:
    new_order = Order.objects.create(user=User.objects.get(username=username))

    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        new_ticket = Ticket(
            order=new_order,
            movie_session=MovieSession.objects.get(
                id=ticket.get("movie_session"),
            ),
            row=ticket.get("row"),
            seat=ticket.get("seat"),
        )
        new_ticket.save()


def get_orders(
        username: Optional[str] = None,
) -> QuerySet[Order]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
