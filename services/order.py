import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    new_order = Order.objects.create(user=user)
    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        movie_s = MovieSession.objects.get(id=ticket.get("movie_session"))
        Ticket.objects.create(
            movie_session=movie_s,
            order=new_order,
            row=ticket.get("row"),
            seat=ticket.get("seat"),
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
