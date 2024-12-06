from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    tickets_obj = [
        Ticket(
            movie_session=MovieSession.objects.get(
                pk=(ticket.get("movie_session"))
            ),
            seat=ticket.get("seat"),
            row=ticket.get("row"),
            order=order
        )
        for ticket in tickets
    ]
    Ticket.objects.bulk_create(tickets_obj)


def get_orders(username: str = None) -> QuerySet:
    query_set = Order.objects.all()

    if username:
        user = get_user_model().objects.get(username=username)
        query_set = query_set.filter(user=user)

    return query_set
