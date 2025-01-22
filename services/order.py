from xmlrpc.client import DateTime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: DateTime = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        tickets_to_create = [
            Ticket(
                seat=ticket["seat"],
                row=ticket["row"],
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"])
            )
            for ticket in tickets
        ]
        Ticket.objects.bulk_create(tickets_to_create)
        if date:
            order.created_at = date
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
