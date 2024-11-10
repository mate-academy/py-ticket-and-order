from django.db import transaction
from django.db.models import QuerySet
from django.utils.datetime_safe import datetime

from db.models import Ticket, Order, User, MovieSession


def create_order(tickets: list[Ticket], username: str,
                 date: datetime = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(
            user=user
        )
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            Ticket.objects.create(
                row=ticket["row"],
                order=order,
                seat=ticket["seat"],
                movie_session=movie_session
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
