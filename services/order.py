from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=(get_user_model().objects.get(username=username))
    )
    if date:
        order.created_at = date
        order.save()

    [Ticket.objects.create(
        movie_session=MovieSession.objects.get(pk=ticket["movie_session"]),
        order=order,
        row=ticket["row"],
        seat=ticket["seat"],
    ) for ticket in tickets]


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
