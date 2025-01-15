from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    order = Order.objects.create(user=User.objects.get(username=username))
    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            row=ticket["row"],
            seat=ticket["seat"],
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
