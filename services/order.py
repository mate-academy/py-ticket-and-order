from datetime import datetime

from django.db import transaction
from django.utils.timezone import make_aware

from db.models import User
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        if date:
            created_at = make_aware(datetime.strptime(date, "%Y-%m-%d %H:%M"))
            order = Order.objects.create(user=user, created_at=created_at)
        else:
            order = Order.objects.create(user=user)

        ticket_objects = [
            Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
                order=order,
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(ticket_objects)
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()