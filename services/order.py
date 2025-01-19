from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, MovieSession, Ticket


def create_order(tickets: list,
                 username: str,
                 date: datetime = None
                 ) -> Order:
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
                id=ticket["movie_session"]
            )
            row = ticket["row"]
            seat = ticket["seat"]

            new_ticket = Ticket(
                row=row,
                seat=seat,
                movie_session=movie_session,
                order=order
            )
            new_ticket.save()

        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
