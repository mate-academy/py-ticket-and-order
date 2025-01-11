from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, User, Order, MovieSession


@transaction.atomic
def create_order(tickets: list,
                 username: str,
                 date: datetime = None
                 ) -> list[Ticket]:
    ticket_objects = []
    user, created = User.objects.get_or_create(username=username)
    order = Order.objects.create(user=user, created_at=date)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        row = ticket["row"]
        seat = ticket["seat"]
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"])
        ticket_objects.append(Ticket(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        ))
    return Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(
            user__username=username).order_by("-created_at")
    return Order.objects.all().order_by("-created_at")
